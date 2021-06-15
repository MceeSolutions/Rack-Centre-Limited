# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class AccessRequest(http.Controller):
    @http.route('/access_request', type="http", auth='user', website=True)
    def index(self, **kw):
        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['name'] = request.env.user.partner_id.name
            if request.env.user.partner_id.parent_id:
                default_values['company_name'] = request.env.user.partner_id.parent_id.name
            else:
                default_values['company_name'] = request.env.user.partner_id.company_name
            default_values['partner_id'] = request.env.user.partner_id.id

        return http.request.render('rc_access_request.create_access_request', {'default_values': default_values})

    @http.route('/create/webaccessrequest', type="http", auth='user', website=True)
    def access_request(self, **kw):
        request.env['access.request'].sudo().create(kw)
        return http.request.render('website_form.contactus_thanks', {})

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
