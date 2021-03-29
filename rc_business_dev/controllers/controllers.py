# -*- coding: utf-8 -*-
# from odoo import http


# class RcBusinessDev(http.Controller):
#     @http.route('/rc_business_dev/rc_business_dev/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rc_business_dev/rc_business_dev/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rc_business_dev.listing', {
#             'root': '/rc_business_dev/rc_business_dev',
#             'objects': http.request.env['rc_business_dev.rc_business_dev'].search([]),
#         })

#     @http.route('/rc_business_dev/rc_business_dev/objects/<model("rc_business_dev.rc_business_dev"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rc_business_dev.object', {
#             'object': obj
#         })
