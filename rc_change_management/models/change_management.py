# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ChangeManagement(models.Model):
    _name = 'change.management.request'
    _description = 'Change Management Request'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('change_coordinator_approved', 'Change Coordinator Approved'),
        ('grc_analyst_approved', 'GRC Analyst Approved'),
        ('service_delivery_approved', 'Service Delivery Approved'),
        ('director_operation_approved', 'Director of Operations Approved'),
        ('approved', 'SDM Implementation Approved'),
        ('reject', 'Rejected'),
        ], string='Approval Status', readonly=False, index=True, copy=False, default='draft', tracking=True)


    ref = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')

    name = fields.Char(string='Summary', required=True, copy=False)
    change_type = fields.Char(string='Change Type')

    change_category = fields.Selection([
        ('onboarding', 'Onboarding'),
        ('decommissioning', 'Decommissioning'),
        ('cross_connect', 'Cross-Connect'),
        ('others', 'Others'),
        ], string='Change Category', copy=False, tracking=True)

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

    change_coordinator = fields.Many2one(comodel_name="res.users", string='Change Coordinator')
    change_manager = fields.Many2one(comodel_name="res.users", string='Change Manager')

    submit_date = fields.Date(string='Submit Date', default=date.today())

    coordinator_group = fields.Char(string='Coordinator Group')
    service = fields.Char(string='Service')
    summary = fields.Char(string='Summary')
    change_class = fields.Char(string='Class')
    change_reason = fields.Char(string='Change Reason')
    target_date = fields.Date(string='Target date')
    impact = fields.Selection([
        ('minor', 'Minor/Localized'),
        ('major', 'Major'),
        ], string='Impact', tracking=True)
    urgency = fields.Selection([
        ('low', 'Low'),
        ('mid', 'Medium'),
        ('high', 'Hign'),
        ], string='Urgency', tracking=True)
    priority = fields.Selection([
        ('0', 'Nil'),
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
        ('4', 'Critical'),
        ], string='Priority', default='1', tracking=True)

    change_type = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
        ], string='Change Type', default='minor', tracking=True, compute='_compute_change_type')

    risk_level = fields.Char(string='Risk Level')
    manager_group = fields.Char(string='Manager Group')

    scheduled_start_date = fields.Date(string='Scheduled Start Date & Time')
    scheduled_end_date = fields.Date(string='Scheduled End Date & time')

    scope_and_impact = fields.Text(string='Scope and Impact of Change')
    docs_impacted = fields.Char(string='Documents Impacted')

    controls_required = fields.Text(string='Controls required')
    financial_impact = fields.Text(string='Financial Impact')
    risk_assessment = fields.Text(string='Risk assessment')

    #Business Justification for the Proposed Change
    business_case_benefits = fields.Text(string='Business Case / Benefits')
    technical_case = fields.Text(string='Technical case, for and against the Change')
    estimated_cost_resources_required = fields.Text(string='Estimated Cost / Resources required for the change.')


    def _compute_change_type(self):
        for type in self:
            if type.priority == '0' or type.priority == '1' or type.priority == '2':
                type.change_type = 'minor'
            else:
                type.change_type = 'major'

    additional_info = fields.Char(string='Additional Information')

    tasks_line_ids = fields.One2many('change.management.tasks', 'change_management_id', string="Tasks", copy=True)

    #Approvals
    change_coordinator_id = fields.Many2one(comodel_name="res.users", string='Change Coordinator', readonly=True)
    change_coordinator_approval_date = fields.Date(string='Change Coordinator Approval Date', readonly=True)

    grc_analyst_id = fields.Many2one(comodel_name="res.users", string='GRC Analyst', readonly=True)
    grc_approval_date = fields.Date(string='GRC Approval Date', readonly=True)

    service_delivery_manager_id = fields.Many2one(comodel_name="res.users", string='Service Delivery Manger', readonly=True)
    service_delivery_approval_date = fields.Date(string='Service Delivery Manger Approval Date', readonly=True)

    director_operation_id = fields.Many2one(comodel_name="res.users", string='Director of Operations', readonly=True)
    director_operation_approval_date = fields.Date(string='Director of Operations Approval Date', readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('change.management') or '/'
        res = super(ChangeManagement, self).create(vals)
        res.action_alert_manager()
        return res 
    
    #alerts cc
    def action_alert_manager(self):
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_ccm')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "A new Change Management Request '{}' with reference '{}', needs review".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to change coordinator
    def button_submit(self):
        self.write({'state': 'submit'})
        #self.submit_date = date.today()
        partner_ids = []
        if not self.change_coordinator:
            raise UserError(_('Please Specify the Change Coordinator.'))
        partner_ids.append(self.change_coordinator.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Change Management Request '{}', needs approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    #submit to GRC Analyst
    def button_change_coordinator_approve(self):
        self.write({'state': 'change_coordinator_approved'})
        self.change_coordinator_id = self.env.uid
        self.change_coordinator_approval_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_grc')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Change Management Request '{}', has been approved by change coordinator and needs your approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to Service Delivery Manger
    def button_grc_analyst_approve(self):
        self.write({'state': 'grc_analyst_approved'})
        self.grc_analyst_id = self.env.uid
        self.grc_approval_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_smd_manager')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Change Management Request '{}', has been approved by GRC Analyst and needs your approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to Director of Operations
    def button_service_delivery_approve(self):
        self.write({'state': 'service_delivery_approved'})
        self.service_delivery_manager_id = self.env.uid
        self.service_delivery_approval_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_doo')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Change Management Request '{}', has been approved by Service Delivery Manger and needs your approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approved by Director of Operations
    def button_director_operation_approve(self):
        self.write({'state': 'director_operation_approved'})
        self.director_operation_id = self.env.uid
        self.director_operation_approval_date = date.today()
        subject = "Change Management Request '{}', has been Approved by Director of Operations".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    #approved by SDM
    def button_approve(self):
        self.write({'state': 'approved'})
        subject = "Change Management Request Implementation for '{}', has been Approved by SDM".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Change Management Request '{}', has been rejected".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

class ChangeManagementTasks(models.Model):
    _name = 'change.management.tasks'
    _description = 'Change Management Tasks'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    change_management_id = fields.Many2one(comodel_name="change.management.request", string='change management')

    name = fields.Char(string='Task Name', required=True)
    summary = fields.Char(string='Task Summary')
    details = fields.Char(string='Task Details / Note')

    start_date = fields.Datetime(string='Scheduled Start Date & Time')
    end_date = fields.Datetime(string='Scheduled End Date & Time')
