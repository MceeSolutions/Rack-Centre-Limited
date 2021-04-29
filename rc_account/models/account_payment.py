# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.payment'

    def action_submit(self):
        self.state = "submit"

    def action_approve(self):
        self.state = "approve" 
