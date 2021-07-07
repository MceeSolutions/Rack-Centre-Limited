# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from werkzeug.utils import redirect

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from datetime import datetime

class DeviceOnboarding(http.Controller):
    @http.route('/device_onboarding', type="http", auth='user', website=True)
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
        return http.request.render('rc_device_onboarding.create_device_onboarding', {'default_values': default_values})

    @http.route('/create/device_onboarding', type="http", auth='user', website=True)
    def device_onboarding(self, **kw):
        
        equipment_manufacturer = request.httprequest.form.getlist('equipment_manufacturer')
        equipment_model = request.httprequest.form.getlist('equipment_model')
        equipment_serial_numbers = request.httprequest.form.getlist('equipment_serial_numbers')
        equipment_power_requirements = request.httprequest.form.getlist('equipment_power_requirements')
        equipment_power = request.httprequest.form.getlist('equipment_power')
        equipment_u_space = request.httprequest.form.getlist('equipment_u_space')
        equipment_power_redendancy = request.httprequest.form.getlist('equipment_power_redendancy')
        equipment_type_of_airflow = request.httprequest.form.getlist('equipment_type_of_airflow')
        equipment_airflow_others = request.httprequest.form.getlist('equipment_airflow_others')
        equipment_rack_mountkits_avilable = request.httprequest.form.getlist('equipment_rack_mountkits_avilable')

        print("<------ equipment_airflow_others ------->", equipment_airflow_others)
    
        task_name = request.httprequest.form.getlist('task_name')
        task_start_date = request.httprequest.form.getlist('task_start_date')
        task_end_date = request.httprequest.form.getlist('task_end_date')
        task_assigned_resource = request.httprequest.form.getlist('task_assigned_resource')

        project_implementation_lines = [(0, 0, {
            'name': task_name,
            'start_date': datetime.fromisoformat(task_start_date),
            'end_date': datetime.fromisoformat(task_end_date),
            'assigned_resource': task_assigned_resource,
        }) for task_name, task_start_date, task_end_date, task_assigned_resource in zip(task_name, task_start_date, task_end_date, task_assigned_resource)]
        
        device_onboarding_lines = [(0, 0, {
            'manufacturer': equipment_manufacturer,
            'model': equipment_model,
            'serial_numbers': equipment_serial_numbers,
            'power_requirements': equipment_power_requirements,
            'power': equipment_power,
            'u_space': equipment_u_space,
            'power_redendancy': equipment_power_redendancy,
            'type_of_airflow': equipment_type_of_airflow,
            'rack_mountkits_avilable': equipment_rack_mountkits_avilable,
        }) for equipment_manufacturer, equipment_model, equipment_serial_numbers, equipment_power_requirements, equipment_power, equipment_u_space, equipment_power_redendancy, equipment_type_of_airflow, equipment_rack_mountkits_avilable in zip(equipment_manufacturer, equipment_model, equipment_serial_numbers, equipment_power_requirements, equipment_power, equipment_u_space, equipment_power_redendancy, equipment_type_of_airflow, equipment_rack_mountkits_avilable)]


        data = {
            'name': kw['name'],
            'user_id': int(kw['user_id']),
            'partner_id': int(kw['partner_id']),
            
            'company_name': kw['company_name'],
            'partner_name': kw['partner_name'],
            'contact_person': kw['contact_person'],
            'contact_email': kw['contact_email'],
            'contact_tel': kw['contact_tel'],
            'date': kw['date'],

            'partner_contact_person': kw['partner_contact_person'],
            'partner_business_address': kw['partner_business_address'],
            'partner_contact_email': kw['partner_contact_email'],
            'partner_contact_tel': kw['partner_contact_tel'],

            'additional_info': kw['additional_info'],

            'device_onboarding_line_ids': device_onboarding_lines,
            'project_plan_line_ids': project_implementation_lines,
        }

        device_onboarding = request.env['device.onboarding'].sudo().create(data)

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
                'res_model': 'device.onboarding',
                'res_id': device_onboarding.id,
                'datas': base64.b64encode(attachment)
            })
        
        # def action_send_notification(self):
        notice = request.env['mail.message'].sudo().create({
                'email_from': request.env.user.partner_id.email, # add the sender email request.env.user.partner_id.email
                'author_id': request.env.user.partner_id.id, # add the creator id
                'model': 'device.onboarding', # model should be mail.channel
                'message_type': 'comment',
                'subtype_id': request.env.ref('mail.mt_comment').id, 
                # 'body': "Body of the message", # here add the message body
                'attachment_ids': attachment_id, #
                #'channel_ids': [(4, self.env.ref('module_name.channel_accountant_group').id)], # This is the channel where you want to send the message and all the users of this channel will receive message
                'res_id': device_onboarding.id, # here add the channel you created.
            })

        return http.request.render('rc_service.request_submited', {})
        
class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'device_onboarding_count' in counters:
            values['device_onboarding_count'] = request.env['device.onboarding'].search_count([])
        return values

    def _device_onboarding_get_page_view_values(self, device_onboarding, access_token, **kwargs):
        values = {
            'page_name': 'Device Onboarding',
            'device_onboarding': device_onboarding,
        }
        return self._get_page_view_values(device_onboarding, access_token, values, 'my_device_onboardings_history', False, **kwargs)
    
    @http.route(['/my/device_onboardings', '/my/device_onboardings/page/<int:page>'], type='http', auth="user", website=True)
    def device_onboarding(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        DeviceOnboarding = request.env['device.onboarding']
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

        # device onboarding count
        device_onboarding_count = DeviceOnboarding.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/device_onboardings",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=device_onboarding_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        device_onboardings = DeviceOnboarding.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_device_onboardings_history'] = device_onboardings.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'device_onboardings': device_onboardings,
            'page_name': 'Device Onboardings',
            'default_url': '/my/device_onboardings',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rc_device_onboarding.portal_my_device_onboardings", values)


    @http.route(['/my/device_onboarding/<int:device_onboarding_id>'], type='http', auth="public", website=True)
    def portal_my_device_onboarding(self, device_onboarding_id=None, access_token=None, **kw):
        try:
            device_onboarding_sudo = self._document_check_access('device.onboarding', device_onboarding_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
            
        values = self._device_onboarding_get_page_view_values(device_onboarding_sudo, access_token, **kw)
        return request.render("rc_device_onboarding.portal_my_device_onboarding", values)