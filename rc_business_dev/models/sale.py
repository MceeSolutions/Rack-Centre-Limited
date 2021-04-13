from odoo import models, fields, api, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('submit', "ELT To Approve"), ('elt_approve', "ELT Approved"), ('sale',)])
    
    def submit(self):
        pass

    def elt_approve(self):
        pass
