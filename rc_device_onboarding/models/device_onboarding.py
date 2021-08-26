# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DeviceOnboarding(models.Model):
    _name = 'device.onboarding'
    _description = 'Device Onboarding'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('finance_approved', 'Finance Approved'),
        ('dc_approved', 'Data Centre Approved'),
        ('approved', 'Service Delivery Approved'),
        ('reject', 'Rejected'),
        ], string='Approval Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    ref = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')

    name = fields.Char(string='Summary', required=True, copy=False)

    partner_id = fields.Many2one(comodel_name="res.partner", string='Requested For')
    user_id = fields.Many2one(comodel_name="res.users", string='Requested By')

    ref = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')

    #Contact Information
    partner_name = fields.Char(string='Partner Name')
    contact_person = fields.Char(string='Contact Person')
    contact_email = fields.Char(string='Email address')
    contact_tel = fields.Char(string='Telephone Numbers')
    date = fields.Char(string='Date')

    company_name = fields.Char(string='Client Organization Name')
    partner_contact_person = fields.Char(string='Contact Person')
    partner_business_address = fields.Char(string='Business Address')
    partner_contact_email = fields.Char(string='Email address')
    partner_contact_tel = fields.Char(string='Telephone Numbers')

    device_onboarding_line_ids = fields.One2many('device.onboarding.lines', 'device_onboarding_id', string="Service Request Lines", copy=True)
    
    #Additional Information
    additional_info = fields.Text(string='Additonal Info')

    project_plan_line_ids = fields.One2many('device.onboarding.project.plan', 'device_onboarding_id', string="Project Implementation Plan", copy=True)

    #Approvals
    finance_manager_id = fields.Many2one(comodel_name="res.users", string='Finanace Manager', readonly=True)
    finance_approval_date = fields.Date(string='Finanace Approval Date', readonly=True)

    data_centre_manager_id = fields.Many2one(comodel_name="res.users", string='Data Centre Manager', readonly=True)
    data_centre_approval_date = fields.Date(string='Data Centre Approval Date', readonly=True)

    command_centre_personnel_id = fields.Many2one(comodel_name="res.users", string='Command Centre', readonly=True)
    command_centre_approval_date = fields.Date(string='Command Centre Approval Date', readonly=True)

    service_delivery_manager_id = fields.Many2one(comodel_name="res.users", string='Service Delivery Manager', readonly=True)
    service_delivery_approval_date = fields.Date(string='Service Delivery Manager Approval Date', readonly=True)
    
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
        
    def _compute_change_type(self):
        for type in self:
            if type.priority == '0' or type.priority == '1' or type.priority == '2':
                type.change_type = 'minor'
            else:
                type.change_type = 'major'

    @api.model
    def create(self, vals):
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('change.request') or '/'
        res = super(DeviceOnboarding, self).create(vals)
        res.action_alert_manager()
        res.create_change_summary()
        return res 
    
    def create_change_summary(self):
        val = {
            'name': self.name,
            'ref': self.ref,
            'change_type': self.change_type,
            'change_category': 'onboarding',
            'partner_id': self.partner_id.id,
            # 'actual_start_date': self.scheduled_start_date,
            # 'actual_end_date': self.scheduled_end_date,
            # 'closure_date_time': self.create_date,
            # 'coordinator_group_id': self.coordinator_group_id.id,
            'submit_date': self.create_date,
            'priority': self.priority,
        }
        self.env['change.summary'].sudo().create(val) 
    
    #alerts cc
    def action_alert_manager(self):
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_ccm')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "A new equipment decommissioning request '{}' with reference '{}', needs review".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    #submit to finance
    def button_submit(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('account.group_account_manager')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "equipment decommissioning request for '{}', needs approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to Data Centre
    def button_finance_approve(self):
        # if self.partner_id.cross_connect_count > self.partner_id.free_cross_connects and self.invoices_count == 0:
        #     raise UserError("This client no longer has free Cross Connects, Hence an invoice should be raised! ")
        self.write({'state': 'finance_approved'})
        self.finance_manager_id = self.env.uid
        self.finance_approval_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_dc')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "equipment decommissioning request for '{}', has been approved by Finance and needs your approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to Service Delivery
    def button_dc_approve(self):
        self.write({'state': 'dc_approved'})
        self.data_centre_manager_id = self.env.uid
        self.data_centre_approval_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_smd_manager')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "equipment decommissioning request for '{}', has been approved by Data Centre and needs your approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approved by Service Delivery
    def button_approve(self):
        self.write({'state': 'approved'})
        self.service_delivery_manager_id = self.env.uid
        self.service_delivery_approval_date = date.today()
        subject = "equipment decommissioning request for '{}', has been Approved by Service Delivery".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "equipment decommissioning request for '{}', has been rejected".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

class DeviceOnboardingLines(models.Model):
    _name = 'device.onboarding.lines'
    _description = 'Device Onboarding Lines'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    device_onboarding_id = fields.Many2one(comodel_name='device.onboarding', string='Device Onboarding')

    #Equipment Description
    manufacturer = fields.Char(string='Manufacturer')
    model = fields.Char(string='Model')
    serial_numbers = fields.Char(string='Serial Number(s)')

    #Power Requirements AC/DC Voltage
    power_requirements = fields.Selection([
        ('ac_single_phase', 'AC: Single Phase'),
        ('three_phase', 'Three Phase'),
        ('dc_voltage', 'DC: Voltage'),
        ], string='Power Requirements AC/DC Voltage')

    # ac_single_phase = fields.Boolean(string='AC: Single Phase')
    # three_phase = fields.Boolean(string='Three Phase')
    # dc_voltage = fields.Boolean(string='DC: Voltage')
    
    power = fields.Char(string='Power (W)')
    u_space = fields.Char(string='U-Space')

    #Power Redundancy Y/N
    power_redendancy = fields.Selection([
        ('single', 'Single'),
        ('dual', 'Dual'),
        ], string='Power Redundancy Y/N')

    #Type of Airflow
    type_of_airflow = fields.Selection([
        ('front_to_back', 'Airflow: Front to Back'),
        ('others', 'Others'),
        ], string='Type of Airflow')
    airflow_others = fields.Char(string='Specify others')
    # airflow_front_to_back = fields.Boolean(string='Airflow: Front to Back')

    #Rack Rails / mount kit / Rack Conversion Kit and IEC C13 - C14 / C19 - C20 Cables Available
    rack_mountkits_avilable = fields.Char(string='Rack Rails / mount kit / Rack Conversion Kit and IEC C13 - C14 / C19 - C20 Cables Available')

class DeviceOnboardingProjectPlan(models.Model):
    _name = 'device.onboarding.project.plan'
    _description = 'Device Onboarding Project Plan' 
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    device_onboarding_id = fields.Many2one(comodel_name="device.onboarding", string='Device Onboarding')

    name = fields.Char(string='Tasks', required=True)

    start_date = fields.Datetime(string='Start Date & Time')
    end_date = fields.Datetime(string='End Date & Time')

    assigned_resource = fields.Char(string='Assigned Resource(s)')