# -*- coding: utf-8 -*-
# from odoo import http


# class RcHrEmployee(http.Controller):
#     @http.route('/rc_hr_employee/rc_hr_employee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rc_hr_employee/rc_hr_employee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rc_hr_employee.listing', {
#             'root': '/rc_hr_employee/rc_hr_employee',
#             'objects': http.request.env['rc_hr_employee.rc_hr_employee'].search([]),
#         })

#     @http.route('/rc_hr_employee/rc_hr_employee/objects/<model("rc_hr_employee.rc_hr_employee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rc_hr_employee.object', {
#             'object': obj
#         })
