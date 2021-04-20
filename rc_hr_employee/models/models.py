# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    #This Archives the employee and send notifications to the respective groups
    def terminate_employee(self):
        self.active = False
        line_manager = self.parent_id.user_id
        department_director = self.department_id.manager_id.user_id
        group_command_center = self.env['ir.model.data'].xmlid_to_object('rc_business_dev.group_command_center')
        partner_ids = []
        if line_manager:
            partner_ids.append(line_manager.partner_id.id)
        if department_director:
            partner_ids.append(department_director.partner_id.id)
        for user in group_command_center.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Employee '{}', from '{}' has resigned".format(self.name, self.department_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)