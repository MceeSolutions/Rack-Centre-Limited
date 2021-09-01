# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EquipmentRelocation(models.Model):
    _name = 'equipment.relocation'
    _description = 'Equipment Relocation'
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

    change_state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled_for_approval', 'Scheduled For Approval'),
        ('scheduled', 'Scheduled'),
        ('request_for_authorization', 'Request For Authorization'),
        ('planning_in_progress', 'Planning In Progress'),
        ('pending', 'Pending'),
        ('implementation_in_progress', 'Implementation In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    change_id = fields.Char(string='Change ID')
    ref = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')

    name = fields.Char(string='Subject / Summary', required=True, copy=False)

    partner_company_id = fields.Many2one(comodel_name="res.partner", string='Client')

    partner_id = fields.Many2one(comodel_name="res.partner", string='Requested For')
    user_id = fields.Many2one(comodel_name="res.users", string='Requested By')

    #Contact Information
    contact_name = fields.Char(string='Name')
    contact_email = fields.Char(string='Email address')
    contact_position = fields.Char(string='Position')
    contact_work_phone = fields.Char(string='Work phone')
    contact_manager_name = fields.Char(string='Manager’s Name')
    contact_manager_phone = fields.Char(string='Manager’s Phone')

    #Equipment Information
    equipment_line_ids = fields.One2many('equipment.relocation.lines', 'equipment_decommissioning_id', string="Equipments", copy=True)
    # equipment_contact_person = fields.Char(string='Equipment contact person')
    # machine_name = fields.Char(string='Machine Name')
    # serial_numbers = fields.Char(string='Serial Number(s)')
    # manufacturer = fields.Char(string='Manufacturer')
    # model = fields.Char(string='Model')
    # operating_system = fields.Char(string='Operating System')
    # ip_address = fields.Char(string='IP Address')

    currect_rack_location = fields.Char(string='Current rack location and Rack Label')
    new_rack_location = fields.Char(string='New rack location and Rack Label')
    relocation_date = fields.Date(string='Relocation date')
    reason = fields.Char(string='Reason')
    relocation_temporary = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Is relocation temporary?')
    expected_return_date = fields.Date(string='Expected return date')
    
    #Additional Information
    additional_info = fields.Text(string='Additonal Info')

    #Approvals
    finance_manager_id = fields.Many2one(comodel_name="res.users", string='Finanace Manager', readonly=True)
    finance_approval_date = fields.Date(string='Finanace Approval Date', readonly=True)

    data_centre_manager_id = fields.Many2one(comodel_name="res.users", string='Data Centre Manager', readonly=True)
    data_centre_approval_date = fields.Date(string='Data Centre Approval Date', readonly=True)

    command_centre_personnel_id = fields.Many2one(comodel_name="res.users", string='Command Centre', readonly=True)
    command_centre_approval_date = fields.Date(string='Command Centre Approval Date', readonly=True)

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

    project_plan_line_ids = fields.One2many('equipment.relocation.project.plan', 'equipment_relocation_id', string="Project Implementation Plan", copy=True)

    coordinator_group_id = fields.Many2one(comodel_name="coordinator.group", string='Coordinator Group')
    manager_group_id = fields.Many2one(comodel_name="res.users", string='Manager Group')

    service = fields.Char(string='Service')
    summary = fields.Char(string='Summary')
    change_class = fields.Char(string='Class')
    change_reason = fields.Char(string='Change Reason')
    target_date = fields.Date(string='Target date')
    impact = fields.Selection([('1', '1-Extensive/Widespread'),('2', '2-Significant/Large'),('3', '3-Moderate/Limited'),('4', '4-Minor/Localized')], string='Impact', tracking=True)
    urgency = fields.Selection([
        ('low', '4-Low'),
        ('mid', '3-Medium'),
        ('high', '2-High'),
        ('critical', '1-Critical'),
        ], string='Urgency', tracking=True)
    change_class = fields.Selection([
        ('emergency', 'Emergency'),
        ('no_impact', 'No Impact'),
        ('normal', 'Normal'),
        ('standard', 'Standard'),
        ], string='Class')

    risk_level = fields.Char(string='Risk Level')

    scheduled_start_date = fields.Datetime(string='Scheduled Start Date & Time')
    scheduled_end_date = fields.Datetime(string='Scheduled End Date & time')
    
    actual_start_date = fields.Datetime(string='Actual Start Date & Time')
    actual_end_date = fields.Datetime(string='Actual End Date & time')
    close_date = fields.Datetime(string='Close Date & time')
    change_coordinator = fields.Char(string='Change Coordinator')
    change_manager = fields.Char(string='Change Manager')
    submit_date = fields.Datetime(string='Submit Date')

    scope_and_impact = fields.Text(string='Scope and Impact of Change')
    docs_impacted = fields.Char(string='Documents Impacted')

    controls_required = fields.Text(string='Controls required')
    financial_impact = fields.Text(string='Financial Impact')
    risk_assessment = fields.Text(string='Risk assessment')

    #Business Justification for the Proposed Change
    business_case_benefits = fields.Text(string='Business Case / Benefits')
    technical_case = fields.Text(string='Technical case, for and against the Change')
    estimated_cost_resources_required = fields.Text(string='Estimated Cost / Resources required for the change.')

    @api.model
    def create(self, vals):
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('change.request') or '/'
        res = super(EquipmentRelocation, self).create(vals)
        res.action_alert_manager()
        res.create_change_summary()
        return res 
    
    def create_change_summary(self):
        val = {
            'name': self.name,
            'ref': self.ref,
            'change_type': self.change_type,
            'change_category': 'relocation',
            'partner_id': self.partner_id.id,
            # 'actual_start_date': self.scheduled_start_date,
            # 'actual_end_date': self.scheduled_end_date,
            # 'closure_date_time': self.create_date,
            # 'coordinator_group_id': self.coordinator_group_id.id,
            'submit_date': self.create_date,
            'priority': self.priority,
        }
        self.env['change.summary'].sudo().create(val) 
        
    @api.onchange('coordinator_group_id')
    def _onchange_partner_id(self):
        self.manager_group_id = self.coordinator_group_id.user_id

    #alerts cc
    def action_alert_manager(self):
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_ccm')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "A new equipment relocation request '{}' with reference '{}', needs review".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def _compute_change_type(self):
        for type in self:
            if type.priority == '0' or type.priority == '1' or type.priority == '2':
                type.change_type = 'minor'
            else:
                type.change_type = 'major'
                
    #submit to finance
    def button_submit(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('account.group_account_manager')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "equipment relocation request for '{}', needs approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to Data Centre
    def button_finance_approve(self):
        # if self.partner_id.remote_hands_count > self.partner_id.free_remote_hands and self.invoices_count == 0:
        #     raise UserError("This client no longer has free remote hands, Hence an invoice should be raised! ")

        self.write({'state': 'finance_approved'})
        self.finance_manager_id = self.env.uid
        self.finance_approval_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_dc')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "equipment relocation request for '{}', has been approved by Finance and needs your approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to Service Delivery
    def button_dc_approve(self):
        self.write({'state': 'dc_approved'})
        self.data_centre_manager_id = self.env.uid
        self.data_centre_approval_date = date.today()

        if not self.implemented_by:
            raise UserError("Please select Implementation Engineer!")

        partner_ids = []
        if not self.implemented_by.user_id:
            raise UserError("This employee is Currently not a User!")

        partner_ids.append(self.implemented_by.user_id.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "equipment relocation request for '{}', has been approved by Data Centre and needs you to begin implementaton".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approved by Service Delivery
    def button_approve(self):
        self.write({'state': 'approved'})
        self.command_centre_personnel_id = self.env.uid
        self.command_centre_approval_date = date.today()
        subject = "equipment relocation request for '{}', has been Approved by Service Delivery".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "equipment relocation request for '{}', has been rejected".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

class EquipmentDecommissioningLines(models.Model):
    _name = 'equipment.relocation.lines'
    _description = 'Relocation Equipments'

    equipment_decommissioning_id = fields.Many2one(comodel_name="equipment.decommissioning", string='Equipment Decommissioning')

    #Equipment Information
    # equipment_contact_person = fields.Char(string='Equipment contact person')
    name = fields.Char(string='Machine Name')
    serial_number = fields.Char(string='Serial Number')
    manufacturer = fields.Char(string='Manufacturer')
    model = fields.Char(string='Model')
    operating_system = fields.Char(string='Operating System')
    ip_address = fields.Char(string='IP Address')

class EquipmentRelocationProjectPlan(models.Model):
    _name = 'equipment.relocation.project.plan'
    _description = 'Equipment Relocation Project Plan'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    equipment_relocation_id = fields.Many2one(comodel_name="equipment.relocation", string='Equipment Relocation')

    name = fields.Char(string='Tasks', required=True)

    start_date = fields.Datetime(string='Start Date & Time')
    end_date = fields.Datetime(string='End Date & Time')

    assigned_resource = fields.Char(string='Assigned Resource(s)')

