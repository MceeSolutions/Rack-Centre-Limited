# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class ChangeManagementRequest(http.Controller):
    @http.route('/change_request', type="http", auth='user', website=True)
    def index(self, **kw):
        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['partner_id'] = request.env.user.partner_id.id
        return http.request.render('rc_change_management.create_change_request', {'default_values': default_values})

    @http.route('/create/change_request', type="http", auth='user', website=True)
    def change_request(self, **kw):
        request.env['change.management.request'].sudo().create(kw)
        return http.request.render('website_form.contactus_thanks', {})

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'change_request_count' in counters:
            values['change_request_count'] = request.env['change.management.request'].search_count([])
        return values

    def _change_request_get_page_view_values(self, change_request, access_token, **kwargs):
        values = {
            'page_name': 'Change Request',
            'change_request': change_request,
        }
        return self._get_page_view_values(change_request, access_token, values, 'my_change_requests_history', False, **kwargs)
    
    @http.route(['/my/change_requests', '/my/change_requests/page/<int:page>'], type='http', auth="user", website=True)
    def index(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        ChangeRequest = request.env['change.management.request']
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
        change_request_count = ChangeRequest.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/change_requests",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=change_request_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        change_requests = ChangeRequest.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_change_requests_history'] = change_requests.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'change_requests': change_requests,
            'page_name': 'Change Requests',
            'default_url': '/my/change_requests',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rc_change_management.portal_my_change_requests", values)


    @http.route(['/my/change_request/<int:change_request_id>'], type='http', auth="public", website=True)
    def portal_my_change_request(self, change_request_id=None, access_token=None, **kw):
        try:
            change_request_sudo = self._document_check_access('change.management.request', change_request_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
            
        values = self._change_request_get_page_view_values(change_request_sudo, access_token, **kw)
        return request.render("rc_change_management.portal_my_change_request", values)