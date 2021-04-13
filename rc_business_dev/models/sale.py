import random
from odoo import models, fields, api, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('submit', "ELT To Approve"), ('elt_approve', "ELT Approved"), ('sale',)])
    discount_above_limit = fields.Boolean(string="self.compute()", compute="check_if_above_limit")

    def check_if_above_limit(self):
        possibilities = True, False
        val = random.choice(possibilities)
        print("Val", val)
        self.discount_above_limit = val

    def submit(self):
        """Submit Request.

        The body of this method is a dummy method that will compute discount_above_limit 
        and return the right state when the button is clicked. It will be cleaned later.
        """
        self.check_if_above_limit()
        state = 'submit' if self.discount_above_limit else 'elt_approve'
        self.state = state

    def elt_approve(self):
        self.state = 'elt_approve'
