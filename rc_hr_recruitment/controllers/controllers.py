# -*- coding: utf-8 -*-
# from odoo import http


# class RcHrRecruitment(http.Controller):
#     @http.route('/rc_hr_recruitment/rc_hr_recruitment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rc_hr_recruitment/rc_hr_recruitment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rc_hr_recruitment.listing', {
#             'root': '/rc_hr_recruitment/rc_hr_recruitment',
#             'objects': http.request.env['rc_hr_recruitment.rc_hr_recruitment'].search([]),
#         })

#     @http.route('/rc_hr_recruitment/rc_hr_recruitment/objects/<model("rc_hr_recruitment.rc_hr_recruitment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rc_hr_recruitment.object', {
#             'object': obj
#         })
