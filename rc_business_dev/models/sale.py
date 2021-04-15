from ast import literal_eval
import random
from odoo import models, fields, api, _
from odoo.tools import safe_eval


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('submit', "Senior Manager To Approve"), ('approve', "ELT To Approve"), ('sale',)])
    discount_above_limit = fields.Boolean(string="Discount Above Limit", compute="check_if_above_limit", copy=False)

    @api.depends("order_line.discount")
    def check_if_above_limit(self):
        discount_limit = self.env['ir.config_parameter'].get_param('rc_business_dev.discount_limit')
        if not discount_limit:
            self.check_if_above_limit = False
            return
        self.discount_above_limit = any(float(discount) > float(discount_limit) for discount in self.order_line.mapped('discount'))

    def submit(self):
        """Submit Request.

        The body of this method is a dummy method that will compute discount_above_limit 
        and return the right state when the button is clicked. It will be cleaned later.
        """
        self.check_if_above_limit()
        state = 'submit'
        self.state = state

    def senior_manager_approve(self):
        if self.discount_above_limit:
            self.state = 'approve'
        else:
            self.action_confirm()

    def elt_approve(self):
        group_data_center = self.env['ir.model.data'].xmlid_to_object('rc_business_dev.group_data_center')
        group_command_center = self.env['ir.model.data'].xmlid_to_object('rc_business_dev.group_command_center')
        group_service_delivery = self.env['ir.model.data'].xmlid_to_object('rc_business_dev.group_service_delivery')
        group_finance = self.env['ir.model.data'].xmlid_to_object('account.group_account_user')
        partners_to_notify = self.env['res.partner'].sudo()
        for user in group_data_center.users:
            partners_to_notify += user.partner_id
        for user in group_command_center.users:
            partners_to_notify += user.partner_id
        for user in group_service_delivery.users:
            partners_to_notify += user.partner_id
        for user in group_finance.users:
            partners_to_notify += user.partner_id
        self.message_subscribe(partner_ids=partners_to_notify.ids)
        subject = "Sales Order {} has been approved".format(self.name)
        self.message_post(subject=subject,body=subject, partner_ids=partners_to_notify.ids)
        self.action_confirm()
