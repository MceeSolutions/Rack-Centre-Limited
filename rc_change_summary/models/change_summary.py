# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ChangeSummary(models.Model):
    _name = 'change.summary'
    _description = 'Change Summary'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    name = fields.Char(string='Summary', required=True)
    ref = fields.Char(string='Change ID', readonly=True, copy=False)
    change_type = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
        ], string='Change Type', default='minor', tracking=True)
    change_category = fields.Selection([
        ('onboarding', 'Onboarding'),
        ('decommissioning', 'Decommissioning'),
        ('relocation', 'Relocation'),
        ('cross_connect', 'Cross-Connect'),
        ('others', 'Others'),
        ], string='Change Category', copy=False)
    partner_id = fields.Many2one(comodel_name="res.partner", string='Client')
    actual_start_date = fields.Date(string='Actual Start Date')
    actual_end_date = fields.Date(string='Actual End Date')
    closure_date_time = fields.Datetime(string='Closure date and time')
    status = fields.Selection([
        ('draft', 'New'),
        ('request_for_authorization', 'Request For Authorization'),
        ('planning_in_progress', 'Planning In Progress'),
        ('cancelled', 'Cancelled'),
        ], string='Status', copy=False, default='draft', tracking=True)

    change_execution_status = fields.Selection([
        ('Completed with Incident', 'Completed with Incident'),
        ('Completed without Incident', 'Completed without Incident'),
        ('Ongoing', 'Ongoing'),
        ], string='Change Execution Status', copy=False, tracking=True)

    coordinator_group_id = fields.Many2one(comodel_name="res.users", string='Co-ordinator Group')
    change_manager_id = fields.Many2one(comodel_name="res.users", string='Change Manager')
    submit_date = fields.Date(string='Submit Date', default=date.today())
    priority = fields.Selection([
        ('0', 'Nil'),
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
        ('4', 'Critical'),
        ], string='Priority', default='1', tracking=True)

    # def create_change_summary(self):
    #     val = {
    #         'name': self.name,
    #         'ref': self.ref,
    #         'change_type': self.change_type,
    #         'change_category': 'cross_connect',
    #         'partner_id': self.partner_id.id,
    #         'actual_start_date': self.actual_start_date,
    #         'actual_end_date': self.actual_end_date,
    #         'closure_date_time': self.closure_date_time,
    #         'coordinator_group_id': self.coordinator_group_id.id,
    #         'submit_date': self.create_date,
    #         'priority': self.priority,
    #     }
    #     self.env['change.summary'].create(val)



