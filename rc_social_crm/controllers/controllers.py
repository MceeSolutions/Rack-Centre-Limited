# -*- coding: utf-8 -*-
# from odoo import http


# class RcSocialCrm(http.Controller):
#     @http.route('/rc_social_crm/rc_social_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rc_social_crm/rc_social_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rc_social_crm.listing', {
#             'root': '/rc_social_crm/rc_social_crm',
#             'objects': http.request.env['rc_social_crm.rc_social_crm'].search([]),
#         })

#     @http.route('/rc_social_crm/rc_social_crm/objects/<model("rc_social_crm.rc_social_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rc_social_crm.object', {
#             'object': obj
#         })
