# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from werkzeug.utils import redirect

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from datetime import datetime

class EquipmentRelocation(http.Controller):
    @http.route('/equipment_relocation', type="http", auth='user', website=True)
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
        return http.request.render('rc_equipment_relocation.create_equipment_relocation', {'default_values': default_values})

    @http.route('/create/equipment_relocation', type="http", auth='user', website=True)
    def equipment_relocation(self, **kw):

        task_name = request.httprequest.form.getlist('task_name')
        task_start_date = request.httprequest.form.getlist('task_start_date')
        task_end_date = request.httprequest.form.getlist('task_end_date')
        task_assigned_resource = request.httprequest.form.getlist('task_assigned_resource')

        lines = [(0, 0, {
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
            
            'equipment_contact_person': kw['equipment_contact_person'],
            'machine_name': kw['machine_name'],
            'serial_numbers': kw['serial_numbers'],
            'manufacturer': kw['manufacturer'],
            'model': kw['model'],
            'operating_system': kw['operating_system'],
            'ip_address': kw['ip_address'],
            'currect_rack_location': kw['currect_rack_location'],
            'new_rack_location': kw['new_rack_location'],
            'relocation_date': kw['relocation_date'],
            'reason': kw['reason'],
            'relocation_temporary': kw['relocation_temporary'],
            'expected_return_date': kw['expected_return_date'],

            'additional_info': kw['additional_info'],
            'project_plan_line_ids': lines,
        }

        equipment_relocation = request.env['equipment.relocation'].sudo().create(data)
        
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
                'res_model': 'equipment.relocation',
                'res_id': equipment_relocation.id,
                'datas': base64.b64encode(attachment)
            })
        
        # def action_send_notification(self):
        notice = request.env['mail.message'].sudo().create({
                'email_from': request.env.user.partner_id.email, # add the sender email request.env.user.partner_id.email
                'author_id': request.env.user.partner_id.id, # add the creator id
                'model': 'equipment.relocation', # model should be mail.channel
                'message_type': 'comment',
                'subtype_id': request.env.ref('mail.mt_comment').id, 
                # 'body': "Body of the message", # here add the message body
                'attachment_ids': attachment_id, #
                #'channel_ids': [(4, self.env.ref('module_name.channel_accountant_group').id)], # This is the channel where you want to send the message and all the users of this channel will receive message
                'res_id': equipment_relocation.id, # here add the channel you created.
            })

        return http.request.render('rc_service.request_submited', {})
        
class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'equipment_relocation_count' in counters:
            values['equipment_relocation_count'] = request.env['equipment.relocation'].search_count([])
        return values

    def _equipment_relocation_get_page_view_values(self, equipment_relocation, access_token, **kwargs):
        values = {
            'page_name': 'Equipment Relocation',
            'equipment_relocation': equipment_relocation,
        }
        return self._get_page_view_values(equipment_relocation, access_token, values, 'my_equipment_relocations_history', False, **kwargs)
    
    @http.route(['/my/equipment_relocations', '/my/equipment_relocations/page/<int:page>'], type='http', auth="user", website=True)
    def index(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        EquipmentRelocation = request.env['equipment.relocation']
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

        # equipment relocation count
        equipment_relocation_count = EquipmentRelocation.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/equipment_relocations",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=equipment_relocation_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        equipment_relocations = EquipmentRelocation.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_equipment_relocations_history'] = equipment_relocations.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'equipment_relocations': equipment_relocations,
            'page_name': 'Equipment Relocations',
            'default_url': '/my/equipment_relocations',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rc_equipment_relocation.portal_my_equipment_relocations", values)


    @http.route(['/my/equipment_relocation/<int:equipment_relocation_id>'], type='http', auth="public", website=True)
    def portal_my_equipment_relocation(self, equipment_relocation_id=None, access_token=None, **kw):
        try:
            equipment_relocation_sudo = self._document_check_access('equipment.relocation', equipment_relocation_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
            
        values = self._equipment_relocation_get_page_view_values(equipment_relocation_sudo, access_token, **kw)
        return request.render("rc_equipment_relocation.portal_my_equipment_relocation", values)