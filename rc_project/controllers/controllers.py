# -*- coding: utf-8 -*-
# from odoo import http


# class RcProject(http.Controller):
#     @http.route('/rc_project/rc_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rc_project/rc_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rc_project.listing', {
#             'root': '/rc_project/rc_project',
#             'objects': http.request.env['rc_project.rc_project'].search([]),
#         })

#     @http.route('/rc_project/rc_project/objects/<model("rc_project.rc_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rc_project.object', {
#             'object': obj
#         })
