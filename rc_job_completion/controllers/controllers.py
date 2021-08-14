# -*- coding: utf-8 -*-
# from odoo import http


# class RcJobCompletion(http.Controller):
#     @http.route('/rc_job_completion/rc_job_completion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rc_job_completion/rc_job_completion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rc_job_completion.listing', {
#             'root': '/rc_job_completion/rc_job_completion',
#             'objects': http.request.env['rc_job_completion.rc_job_completion'].search([]),
#         })

#     @http.route('/rc_job_completion/rc_job_completion/objects/<model("rc_job_completion.rc_job_completion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rc_job_completion.object', {
#             'object': obj
#         })
