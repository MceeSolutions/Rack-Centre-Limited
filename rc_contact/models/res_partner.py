
from odoo import fields, models

class Partner(models.Model):
    _inherit = "res.partner"

    industry_id = fields.Many2one(comodel_name='res.partner.industry', string='Vertical')
    lead_source = fields.Char(string='Lead Source')