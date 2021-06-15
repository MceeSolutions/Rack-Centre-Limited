# -*- coding: utf-8 -*-
# from odoo import http


# class RcDailyWalkaround(http.Controller):
#     @http.route('/rc_daily_walkaround/rc_daily_walkaround/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rc_daily_walkaround/rc_daily_walkaround/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rc_daily_walkaround.listing', {
#             'root': '/rc_daily_walkaround/rc_daily_walkaround',
#             'objects': http.request.env['rc_daily_walkaround.rc_daily_walkaround'].search([]),
#         })

#     @http.route('/rc_daily_walkaround/rc_daily_walkaround/objects/<model("rc_daily_walkaround.rc_daily_walkaround"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rc_daily_walkaround.object', {
#             'object': obj
#         })
