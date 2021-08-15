
from odoo import fields, models

class Partner(models.Model):
    _inherit = "res.partner"

    industry_id = fields.Many2one(comodel_name='res.partner.industry', string='Vertical')
    lead_source = fields.Char(string='Lead Source')
    

    legacy_create_date = fields.Datetime('Creation Date', readonly=False, copy=False)
    legacy_created_by = fields.Char('Created By', readonly=False, copy=False, index=True)
