from odoo import models, fields, api


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    state = fields.Selection(selection_add=[('submit', 'Submitted'), ('approve', 'Approved'), ('open',)])