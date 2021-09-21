#-*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = "res.partner"

    industry_id = fields.Many2one(comodel_name='res.partner.industry', string='Vertical')
    lead_source = fields.Char(string='Lead Source')
    linkedin_url = fields.Char(string='LinkedIn URL')
    linkedin_connection_sales = fields.Char(string='LinkedIn connection by sales team')
    
    import_create_date = fields.Datetime('Creation Date', readonly=False, copy=False)
    import_created_by = fields.Char('Created By', readonly=False, copy=False)

