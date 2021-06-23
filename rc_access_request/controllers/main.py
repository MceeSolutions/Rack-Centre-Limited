# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from werkzeug.utils import redirect

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from datetime import datetime

class AccessRequest(http.Controller):
    @http.route('/access_request', type="http", auth='user', website=True)
    def index(self, **kw):
        access_category_id = http.request.env['access.category'].sudo().search([])
        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['name'] = request.env.user.partner_id.name
            if request.env.user.partner_id.parent_id:
                default_values['partner_id'] = int(request.env.user.partner_id.parent_id.id)
            else:
                default_values['partner_id'] = int(request.env.user.partner_id.id)
            default_values['user_id'] = request.env.user.id
            default_values['requested_for_id'] = request.env.user.partner_id.id
            if request.env.user.partner_id.parent_id:
                default_values['company_name'] = request.env.user.partner_id.parent_id.name
            else:
                default_values['company_name'] = request.env.user.partner_id.company_name
            default_values['partner_id'] = request.env.user.partner_id.id

        return http.request.render('rc_access_request.create_access_request', {'default_values': default_values, 'access_category_id':access_category_id})

    @http.route('/create/webaccessrequest', type="http", auth='user', website=True)
    def access_request(self, **kw):
        start_date = datetime.fromisoformat(kw['start_date'])
        end_date = datetime.fromisoformat(kw['end_date'])
        
        office_building = kw.get('office_building')
        dx_unit = kw.get('dx_unit')
        data_centre = kw.get('data_centre')
        dc_surroundings = kw.get('dc_surroundings')
        staging_area = kw.get('staging_area')
        diesel_generator_area = kw.get('diesel_generator_area')
        bcp_building = kw.get('bcp_building')

        visitor_designation = request.httprequest.form.getlist('visitor_designation')
        visitor_phone = request.httprequest.form.getlist('visitor_phone')
        visitor_name = request.httprequest.form.getlist('visitor_name')
        visitor_company = request.httprequest.form.getlist('visitor_company')

        lines = [(0, 0, {
            'name': visitor_name,
            'designation': visitor_designation,
            'phone': visitor_phone,
            'company': visitor_company,
        }) for visitor_name, visitor_designation, visitor_phone, visitor_company in zip(visitor_name, visitor_phone, visitor_designation, visitor_company)]
        
        data = {
            'name': kw['name'],
            'partner_id': int(kw['partner_id']),
            'company_name': kw['company_name'],
            'designation': kw['designation'],
            'purpose': kw['purpose'],

            'office_building': office_building,
            'data_centre': data_centre,
            'dx_unit': dx_unit,
            'dc_surroundings': dc_surroundings,
            'staging_area': staging_area,
            'diesel_generator_area': diesel_generator_area,
            'bcp_building': bcp_building,

            'access_category_id': kw['access_category_id'],
            'requested_for_id': kw['requested_for_id'],
            'user_id': int(kw['user_id']),
            'additional_info': kw['additional_info'],
            'start_date': start_date,
            'end_date': end_date,
            'access_request_line_ids': lines,
        }

        access_request = request.env['access.request'].sudo().create(data)
        
        if kw.get('health_screening_form', False):
            IrAttachment = request.env['ir.attachment']
            name = kw.get('health_screening_form').filename
            file = kw.get('health_screening_form')
            attachment = file.read()
            attachment_id = IrAttachment.sudo().create({
                'name': name,
                'store_fname': name,
                'res_name': name,
                'type': 'binary',
                'res_model': 'equipment.relocation',
                'res_id': access_request.id,
                'datas': base64.b64encode(attachment)
            })
        
        # def action_send_notification(self):
        notice = request.env['mail.message'].sudo().create({
                'email_from': request.env.user.partner_id.email, # add the sender email request.env.user.partner_id.email
                'author_id': request.env.user.partner_id.id, # add the creator id
                'model': 'access.request', # model should be mail.channel
                'message_type': 'comment',
                'subtype_id': request.env.ref('mail.mt_comment').id, 
                # 'body': "Body of the message", # here add the message body
                'attachment_ids': attachment_id, #
                #'channel_ids': [(4, self.env.ref('module_name.channel_accountant_group').id)], # This is the channel where you want to send the message and all the users of this channel will receive message
                'res_id': access_request.id, # here add the channel you created.
            })

        return http.request.render('rc_service.request_submited', {})

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'access_request_count' in counters:
            values['access_request_count'] = request.env['access.request'].search_count([])
        return values

    def _access_requet_get_page_view_values(self, access_request, access_token, **kwargs):
        values = {
            'page_name': 'Access Requests',
            'access_request': access_request,
        }
        return self._get_page_view_values(access_request, access_token, values, 'my_access_requests_history', False, **kwargs)
    
    @http.route(['/my/access_requests', '/my/access_requets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_access_requets(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        AccessRequest = request.env['access.request']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        searchbar_groupby = {
            # 'none': {'input': 'none', 'label': _('None')},
            # 'project': {'input': 'project', 'label': _('Project')},
            'date': {'input': 'create_date', 'label': _('Date')},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # projects count
        access_request_count = AccessRequest.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/access_requests",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=access_request_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        access_requests = AccessRequest.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_access_requests_history'] = access_requests.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'access_requests': access_requests,
            'page_name': 'Access Requests',
            'default_url': '/my/access_requests',
            'pager': pager,
            # 'searchbar_groupby': searchbar_groupby,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rc_access_request.portal_my_access_requests", values)


    @http.route(['/my/access_request/<int:access_request_id>'], type='http', auth="public", website=True)
    def portal_my_access_request(self, access_request_id=None, access_token=None, **kw):
        try:
            access_request_sudo = self._document_check_access('access.request', access_request_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
            
        values = self._access_requet_get_page_view_values(access_request_sudo, access_token, **kw)
        return request.render("rc_access_request.portal_my_access_request", values)
