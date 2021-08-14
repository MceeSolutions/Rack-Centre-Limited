# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class MaterialGatepass(http.Controller):
    @http.route('/material_gatepass', type="http", auth='user', website=True)
    def index(self, **kw):
        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            #default_values['partner_id'] = request.env.user.partner_id.id
            default_values['partner_id'] = request.env.user.id
            default_values['partner_name'] = request.env.user.partner_id.name
            default_values['user_id'] = request.env.user.id
            if request.env.user.partner_id.parent_id:
                default_values['company_name'] = request.env.user.partner_id.parent_id.name
            else:
                default_values['company_name'] = request.env.user.partner_id.company_name
        return http.request.render('rc_cc_material_gatepass.create_material_gatepass', {'default_values': default_values})

    @http.route('/create/material_gatepass', type="http", auth='user', website=True)
    def material_gatepass(self, **kw):

        material_description = request.httprequest.form.getlist('material_description')
        material_qty_request = request.httprequest.form.getlist('material_qty_request')
        material_serial_no = request.httprequest.form.getlist('material_serial_no')

        lines = [(0, 0, {
            'description': material_description,
            'qty_request': material_qty_request,
            'serial_no': material_serial_no,
        }) for material_description, material_qty_request, material_serial_no in zip(material_description, material_qty_request, material_serial_no)]

        data = {
            'name': kw['name'],
            'user_id': int(kw['user_id']),
            'partner_id': int(kw['partner_id']),
            'company_name': kw['company_name'],
            'material_from': kw['from'],
            'material_to': kw['to'],
            'request_date': kw['request_date'],
            'summary': kw['additional_info'],
            'line_ids': lines,
        }

        material_gatepass = request.env['material.gatepass'].sudo().create(data)
        return http.request.render('rc_service.request_submited', {})

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'material_gatepass_count' in counters:
            values['material_gatepass_count'] = request.env['material.gate.pass'].search_count([])
        return values

    def _material_gatepass_get_page_view_values(self, material_gatepass, access_token, **kwargs):
        values = {
            'page_name': 'Material Gatepass',
            'material_gatepass': material_gatepass,
        }
        return self._get_page_view_values(material_gatepass, access_token, values, 'my_material_gatepasses_history', False, **kwargs)
    
    @http.route(['/my/material_gatepasses', '/my/material_gatepasses/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_material_gatepasses(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        MaterialGatepass = request.env['material.gate.pass']
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

        # Material Gatepass count
        material_gatepass_count = MaterialGatepass.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/material_gatepasses",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=material_gatepass_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        material_gatepasses = MaterialGatepass.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_material_gatepasses_history'] = material_gatepasses.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'material_gatepasses': material_gatepasses,
            'page_name': 'Material Gatepasses',
            'default_url': '/my/material_gatepasses',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rc_cc_material_gatepass.portal_my_material_gatepasses", values)


    @http.route(['/my/material_gatepass/<int:material_gatepass_id>'], type='http', auth="public", website=True)
    def portal_my_material_gatepass(self, material_gatepass_id=None, access_token=None, **kw):
        try:
            material_gatepass_sudo = self._document_check_access('material.gate.pass', material_gatepass_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
            
        values = self._material_gatepass_get_page_view_values(material_gatepass_sudo, access_token, **kw)
        return request.render("rc_cc_material_gatepass.portal_my_material_gatepass", values)