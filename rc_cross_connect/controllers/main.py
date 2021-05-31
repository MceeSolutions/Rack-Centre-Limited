# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class CrossConnect(http.Controller):
    @http.route('/cross_connect', type="http", auth='user', website=True)
    def index(self, **kw):
        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['partner_id'] = request.env.user.partner_id.id
        return http.request.render('rc_cross_connect.create_cross_connect', {'default_values': default_values})

    @http.route('/create/cross_connect', type="http", auth='user', website=True)
    def cross_connect(self, **kw):
        request.env['cross.connect'].sudo().create(kw)
        return http.request.render('rc_cross_connect.cross_connect_submited', {})

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'cross_connect_count' in counters:
            values['cross_connect_count'] = request.env['cross.connect'].search_count([])
        return values

    def _cross_connect_get_page_view_values(self, cross_connect, access_token, **kwargs):
        values = {
            'page_name': 'Cross Connects',
            'cross_connect': cross_connect,
        }
        return self._get_page_view_values(cross_connect, access_token, values, 'my_cross_connects_history', False, **kwargs)
    
    @http.route(['/my/cross_connects', '/my/cross_connects/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_cross_connects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        CrossConnect = request.env['cross.connect']
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
        cross_connect_count = CrossConnect.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/cross_connects",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=cross_connect_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        cross_connects = CrossConnect.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_cross_connects_history'] = cross_connects.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'cross_connects': cross_connects,
            'page_name': 'Cross Connects',
            'default_url': '/my/cross_connects',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rc_cross_connect.portal_my_cross_connects", values)


    @http.route(['/my/cross_connect/<int:cross_connect_id>'], type='http', auth="public", website=True)
    def portal_my_cross_connect(self, cross_connect_id=None, access_token=None, **kw):
        try:
            cross_connect_sudo = self._document_check_access('cross.connect', cross_connect_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
            
        values = self._cross_connect_get_page_view_values(cross_connect_sudo, access_token, **kw)
        return request.render("rc_cross_connect.portal_my_cross_connect", values)