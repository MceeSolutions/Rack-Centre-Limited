from datetime import date
from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if picking_type_id == '':
            self.notify_project_manager()
        return res

    def notify_project_manager(self):
        group_project_manager = self.env['ir.model.data'].xmlid_to_object('project.group_project_manager')
        partners_to_notify = self.env['res.partner'].sudo()
        for user in group_data_center.users:
            partners_to_notify += user.partner_id
        self.message_subscribe(partner_ids=partners_to_notify.ids)
        subject = "Receipt #{} has been validated".format(self.name)
        self.message_post(subject=subject, body=subject, partner_ids=partners_to_notify.ids)
        return True