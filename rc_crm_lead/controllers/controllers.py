 # -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm

class WebsiteCrmLead(http.Controller):
    @http.route('/contactus', type='http', auth="public", website=True)
    def index(self, **kw):
        industry_id = http.request.env['res.partner.industry'].sudo().search([])
        return http.request.render("rc_crm_lead.rc_crm_contactus_form", {'industry_id':industry_id})