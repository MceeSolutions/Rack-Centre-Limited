# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from werkzeug.utils import redirect

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from datetime import datetime


class EquipmentDecommissioning(http.Controller):
    @http.route('/equipment_decommissioning', type="http", auth='user', website=True)
    def index(self, **kw):
        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['partner_id'] = request.env.user.partner_id.id
            default_values['user_id'] = request.env.user.id
            default_values['name'] = request.env.user.partner_id.name
            default_values['email'] = request.env.user.partner_id.email
            default_values['phone'] = request.env.user.partner_id.phone
            if request.env.user.partner_id.parent_id:
                default_values['company_name'] = request.env.user.partner_id.parent_id.name
            else:
                default_values['company_name'] = request.env.user.partner_id.company_name
        return http.request.render('rc_equipment_decommissioning.create_equipment_decommissioning', {'default_values': default_values})

    @http.route('/create/equipment_decommissioning', type="http", auth='user', website=True)
    def equipment_decommissioning(self, **kw):
        
        machine_name = request.httprequest.form.getlist('machine_name')
        serial_number = request.httprequest.form.getlist('serial_number')
        manufacturer = request.httprequest.form.getlist('manufacturer')
        model = request.httprequest.form.getlist('model')
        operating_system = request.httprequest.form.getlist('operating_system')
        ip_address = request.httprequest.form.getlist('ip_address')

        equipment_lines = [(0, 0, {
            'name': machine_name,
            'serial_number': serial_number,
            'manufacturer': manufacturer,
            'model': model,
            'operating_system': operating_system,
            'ip_address': ip_address,
        }) for machine_name, serial_number, manufacturer, model, operating_system, ip_address in zip(machine_name, serial_number, manufacturer, model, operating_system, ip_address)]
        

        task_name = request.httprequest.form.getlist('task_name')
        task_start_date = request.httprequest.form.getlist('task_start_date')
        task_end_date = request.httprequest.form.getlist('task_end_date')
        task_assigned_resource = request.httprequest.form.getlist('task_assigned_resource')

        project_plan_lines = [(0, 0, {
            'name': task_name,
            'start_date': datetime.fromisoformat(task_start_date),
            'end_date': datetime.fromisoformat(task_end_date),
            'assigned_resource': task_assigned_resource,
        }) for task_name, task_start_date, task_end_date, task_assigned_resource in zip(task_name, task_start_date, task_end_date, task_assigned_resource)]

        data = {
            'name': kw['name'],
            'user_id': int(kw['user_id']),
            'partner_id': int(kw['partner_id']),
            
            'contact_name': kw['contact_name'],
            'contact_email': kw['contact_email'],
            'contact_position': kw['contact_position'],
            'contact_work_phone': kw['contact_work_phone'],
            'contact_manager_name': kw['contact_manager_name'],
            'contact_manager_phone': kw['contact_manager_phone'],
            
            # 'equipment_contact_person': kw['equipment_contact_person'],
            # 'machine_name': kw['machine_name'],
            # 'serial_numbers': kw['serial_numbers'],
            # 'manufacturer': kw['manufacturer'],
            # 'model': kw['model'],
            # 'operating_system': kw['operating_system'],
            # 'ip_address': kw['ip_address'],
            'currect_rack_location': '(Floor):' + kw['src_floor'] + '/' + '(IT Room):' + kw['src_it_room'] + '/' + '(Rack Location):' + kw['src_rack_location'] + '/' + '(Rack Number):' + kw['src_rack_number'] + '/' + '(U-Space):' + kw['src_uspace'],
            # 'currect_rack_location': kw['currect_rack_location'],

            'decommissioning_reason': kw['decommissioning_reason'],
            'plan_to_return': kw['plan_to_return'],
            'expected_return_date': kw['expected_return_date'],

            'additional_info': kw['additional_info'],
            'equipment_line_ids': equipment_lines,
            'project_plan_line_ids': project_plan_lines,
        }

        equipment_decommissioning = request.env['equipment.decommissioning'].sudo().create(data)
        
        if kw.get('topology_planning_form', False):
            IrAttachment = request.env['ir.attachment']
            name = kw.get('topology_planning_form').filename
            file = kw.get('topology_planning_form')
            attachment = file.read()
            attachment_id = IrAttachment.sudo().create({
                'name': name,
                'store_fname': name,
                'res_name': name,
                'type': 'binary',
                'res_model': 'equipment.decommissioning',
                'res_id': equipment_decommissioning.id,
                'datas': base64.b64encode(attachment)
            })
        
        # def action_send_notification(self):
        notice = request.env['mail.message'].sudo().create({
                'email_from': request.env.user.partner_id.email, # add the sender email request.env.user.partner_id.email
                'author_id': request.env.user.partner_id.id, # add the creator id
                'model': 'equipment.decommissioning', # model should be mail.channel
                'message_type': 'comment',
                'subtype_id': request.env.ref('mail.mt_comment').id, 
                # 'body': "Body of the message", # here add the message body
                'attachment_ids': attachment_id, #
                #'channel_ids': [(4, self.env.ref('module_name.channel_accountant_group').id)], # This is the channel where you want to send the message and all the users of this channel will receive message
                'res_id': equipment_decommissioning.id, # here add the channel you created.
            })

        return http.request.render('rc_service.request_submited', {})
        
class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'equipment_decommissioning_count' in counters:
            values['equipment_decommissioning_count'] = request.env['equipment.decommissioning'].search_count([])
        return values

    def _equipment_decommissioning_get_page_view_values(self, equipment_decommissioning, access_token, **kwargs):
        values = {
            'page_name': 'Equipment Decommissioning',
            'equipment_decommissioning': equipment_decommissioning,
        }
        return self._get_page_view_values(equipment_decommissioning, access_token, values, 'my_equipment_decommissionings_history', False, **kwargs)
    
    @http.route(['/my/equipment_decommissionings', '/my/equipment_decommissionings/page/<int:page>'], type='http', auth="user", website=True)
    def equipment_decommissionings(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        EquipmentDecommissioning = request.env['equipment.decommissioning']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # equipment decommissioning count
        equipment_decommissioning_count = EquipmentDecommissioning.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/equipment_decommissionings",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=equipment_decommissioning_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        equipment_decommissionings = EquipmentDecommissioning.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_equipment_decommissionings_history'] = equipment_decommissionings.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'equipment_decommissionings': equipment_decommissionings,
            'page_name': 'Equipment Decommissionings',
            'default_url': '/my/equipment_decommissionings',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rc_equipment_decommissioning.portal_my_equipment_decommissionings", values)


    @http.route(['/my/equipment_decommissioning/<int:equipment_decommissioning_id>'], type='http', auth="public", website=True)
    def portal_my_equipment_decommissioning(self, equipment_decommissioning_id=None, access_token=None, **kw):
        try:
            equipment_decommissioning_sudo = self._document_check_access('equipment.decommissioning', equipment_decommissioning_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
            
        values = self._equipment_decommissioning_get_page_view_values(equipment_decommissioning_sudo, access_token, **kw)
        return request.render("rc_equipment_decommissioning.portal_my_equipment_decommissioning", values)