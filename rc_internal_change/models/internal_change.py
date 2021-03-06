# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InternalChange(models.Model):
    _name = 'internal.change'
    _description = 'Internal Change'
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

    name = fields.Char(string='Subject / Summary', required=True, copy=False)

    partner_id = fields.Many2one(comodel_name="res.partner", string='Client')

    change_id = fields.Char(string='Change ID')
    ref = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')

    #client category
    client_cl = fields.Boolean(string='Client (Cl)')
    carrier_ca = fields.Boolean(string='Carrier (Ca)')
    indirect_client = fields.Boolean(string='Indirect Client (IDC)')
    ixpn = fields.Boolean(string='IXPN')

    #Request Type
    new_installation = fields.Boolean(string='New Installation')
    decommissioning = fields.Boolean(string='Decommissioning')
    relocation = fields.Boolean(string='Relocation')

    #Service Options
    cl_ca = fields.Boolean(string='Cl-Ca')
    ca_cl = fields.Boolean(string='Ca-Cl')
    cl_cl = fields.Boolean(string='Cl-Cl')
    ca_ca = fields.Boolean(string='Ca-Ca')
    ca_ixpn = fields.Boolean(string='Ca-IXPN')
    cl_ixpn = fields.Boolean(string='Cl-IXPN')
    ixpn_ca = fields.Boolean(string='IXPN-CA')
    ixpn_cl = fields.Boolean(string='IXPN-Cl')

    #Technical Details
    requester = fields.Boolean(string='Requester')
    destination = fields.Boolean(string='Destination')

    fibre = fields.Boolean(string='Fibre (MM/SMF)')
    cat6 = fields.Boolean(string='CAT 6 (RJ45)')

    number_of_xconnect = fields.Integer(string='Number of X-connect')
    location_from = fields.Char(string='Location (From)')
    location_to = fields.Char(string='Location (To)')

    #Billing information
    billed_to_requester = fields.Boolean(string='Billed to Requester')
    billed_to_recipient = fields.Boolean(string='Billed to Recipient')
    waived = fields.Boolean(string='Waived')

    #Comment/Additional information
    additional_info = fields.Text(string='Comment/Additional information')

    #invoice
    invoices_count = fields.Integer(string="Invoices")

    #Approvals
    finance_manager_id = fields.Many2one(comodel_name="res.users", string='Finanace Manager', readonly=True)
    finance_approval_date = fields.Date(string='Finanace Approval Date', readonly=True)

    data_centre_manager_id = fields.Many2one(comodel_name="res.users", string='Data Centre Manager', readonly=True)
    data_centre_approval_date = fields.Date(string='Data Centre Date', readonly=True)

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

    change_coordinator = fields.Char(string='Change Coordinator')
    change_manager = fields.Char(string='Change Manager')

    submit_date = fields.Datetime(string='Submit Date')

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

    scope_and_impact = fields.Text(string='Scope and Impact of Change')
    docs_impacted = fields.Char(string='Documents Impacted')

    controls_required = fields.Text(string='Controls required')
    financial_impact = fields.Text(string='Financial Impact')
    risk_assessment = fields.Text(string='Risk assessment')

    #Business Justification for the Proposed Change
    business_case_benefits = fields.Text(string='Business Case / Benefits')
    technical_case = fields.Text(string='Technical case, for and against the Change')
    estimated_cost_resources_required = fields.Text(string='Estimated Cost / Resources required for the change.')

    additional_info = fields.Text(string='Comment/Additional information')

    @api.model
    def create(self, vals):
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('change.request') or '/'
        res = super(InternalChange, self).create(vals)
        res.create_change_summary()
        return res 

    def create_change_summary(self):
        val = {
            'name': self.name,
            'ref': self.ref,
            'change_type': self.change_type,
            'change_category': 'others',
            'partner_id': self.partner_id.id,
            'actual_start_date': self.scheduled_start_date,
            'actual_end_date': self.scheduled_end_date,
            'closure_date_time': self.create_date,
            'coordinator_group_id': self.coordinator_group_id.id,
            'submit_date': self.create_date,
            'priority': self.priority,
        }
        self.env['change.summary'].sudo().create(val)

    @api.onchange('coordinator_group_id')
    def _onchange_partner_id(self):
        self.manager_group_id = self.coordinator_group_id.user_id

    # #alerts cc
    # def action_alert_manager(self):
    #     group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_ccm')
    #     partner_ids = []
    #     for user in group_id.users:
    #         partner_ids.append(user.partner_id.id)
    #     self.message_subscribe(partner_ids=partner_ids)
    #     subject = "A new Internal Change Request '{}' with reference '{}', needs review".format(self.name, self.ref)
    #     self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    # def count_invoices(self):
    #     invoice_obj = self.env['account.move']
    #     for invoice in self:
    #         domain = [('internal_change_id', '=', invoice.id)]
    #         invoice_obj_ids = invoice_obj.search(domain)
    #         browseed_ids = invoice_obj.browse(invoice_obj_ids)
    #         invoice_obj_count = 0
    #         for id in browseed_ids:
    #             invoice_obj_count+=1
    #         invoice.invoices_count= invoice_obj_count
    #     return True

    # def action_view_invoices(self):
    #     invoice = self.env['account.move'].search([('internal_change_id', '=', self.id)])
    #     action = self.env.ref('account.action_move_out_invoice_type')
    #     result = action.read()[0]
    #     if self.invoices_count != 1:
    #         result['domain'] = "[('id', 'in', " + str(invoice.ids) + ")]"
    #     elif self.invoices_count == 1:
    #         res = self.env.ref('account.view_move_form', False)
    #         result['views'] = [(res and res.id or False, 'form')]
    #         result['res_id'] = invoice.id
    #     return result

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
        if self.coordinator_group_id.user_id:
            partner_ids.append(self.coordinator_group_id.user_id.partner_id.id)
        else:
            for user in group_id.users:
                partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Internal Change Request for '{}', needs approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to Data Centre
    def button_finance_approve(self):
        # if self.partner_id.internal_change_count > self.partner_id.free_internal_changes and self.invoices_count == 0:
        #     raise UserError("This client no longer has free Internal Changes, Hence an invoice should be raised! ")

        self.write({'state': 'finance_approved'})
        self.finance_manager_id = self.env.uid
        self.finance_approval_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_dc')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Internal Change Request for '{}', has been approved by Finance and needs your approval".format(self.ref)
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
        subject = "Internal Change Request for '{}', has been approved by Data Centre and needs your approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approved by Service Delivery
    def button_approve(self):
        self.write({'state': 'approved'})
        self.service_delivery_manager_id = self.env.uid
        self.service_delivery_approval_date = date.today()
        subject = "Internal Change Request for '{}', has been Approved by Service Delivery".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Internal Change Request for '{}', has been rejected".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

    # #To create invoice
    # def create_invoice(self):
    #     """
    #     Method to open create invoice form
    #     """

    #     view_ref = self.env['ir.model.data'].get_object_reference('account', 'view_move_form')
    #     view_id = view_ref[1] if view_ref else False
         
    #     res = {
    #         'type': 'ir.actions.act_window',
    #         'name': ('Customer Invoice'),
    #         'res_model': 'account.move',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'view_id': view_id,
    #         'target': 'current',
    #         'context': {
    #             'default_partner_id': self.partner_id.id, 
    #             'default_internal_change_id': self.id, 
    #             'default_move_type': 'out_invoice',
    #             }
    #     }
        
    #     return res