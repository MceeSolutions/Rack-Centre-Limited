# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class RemoteHand(http.Controller):
    @http.route('/remote_hand', type="http", auth='user', website=True)
    def index(self, **kw):
        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['partner_id'] = request.env.user.partner_id.id
            default_values['user_id'] = request.env.user.id
        return http.request.render('rc_remote_hand.create_remote_hand', {'default_values': default_values})

    @http.route('/create/remote_hand', type="http", auth='user', website=True)
    def remote_hand(self, **kw):
        request.env['remote.hand'].sudo().create(kw)
        return http.request.render('rc_service.request_submited', {})

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'remote_hand_count' in counters:
            values['remote_hand_count'] = request.env['remote.hand'].search_count([])
        return values

    def _remote_hand_get_page_view_values(self, remote_hand, access_token, **kwargs):
        values = {
            'page_name': 'Remote Hand',
            'remote_hand': remote_hand,
        }
        return self._get_page_view_values(remote_hand, access_token, values, 'my_remote_hands_history', False, **kwargs)
    
    @http.route(['/my/remote_hands', '/my/remote_hands/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_remote_hands(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        RemoteHand = request.env['remote.hand']
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

        # remote hand count
        remote_hand_count = RemoteHand.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/remote_hands",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=remote_hand_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        remote_hands = RemoteHand.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_remote_hands_history'] = remote_hands.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'remote_hands': remote_hands,
            'page_name': 'Remote Hands',
            'default_url': '/my/remote_hands',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rc_remote_hand.portal_my_remote_hands", values)


    @http.route(['/my/remote_hand/<int:remote_hand_id>'], type='http', auth="public", website=True)
    def portal_my_remote_hand(self, remote_hand_id=None, access_token=None, **kw):
        try:
            remote_hand_sudo = self._document_check_access('remote.hand', remote_hand_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
            
        values = self._remote_hand_get_page_view_values(remote_hand_sudo, access_token, **kw)
        return request.render("rc_remote_hand.portal_my_remote_hand", values)