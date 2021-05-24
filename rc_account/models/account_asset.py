from odoo import models, fields, api


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    state = fields.Selection(selection_add=[('submit', 'Submitted'), ('approve', 'Approved'), ('open',)])

    def action_submit(self):
        self.state = 'submit'

    def action_approve(self):
        self.state = 'approve'