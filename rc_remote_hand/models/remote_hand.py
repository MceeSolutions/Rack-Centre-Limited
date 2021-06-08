# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class RemoteHand(models.Model):
    _name = 'remote.hand'
    _description = 'Remote Hand'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    name = fields.Char(string='Subject', required=True, copy=False)
    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('finance_approved', 'Finance Approved'),
        ('dc_approved', 'Data Centre Approved'),
        ('approved', 'Service Delivery Approved'),
        ('reject', 'Rejected'),
        ], string='Approval Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    ref = fields.Char(string='Service ID', readonly=True, required=True, index=True, copy=False, default='New')
    legend = fields.Char(string='Legend')
    reason_for_visit = fields.Char(string='Reason For Visit')
    user_id = fields.Many2one(comodel_name="res.users", string='Requested By')
    weekday = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ], string='Weekday')

    partner_id = fields.Many2one(comodel_name="res.partner", string='Requested For')
    implemented_by = fields.Many2one(comodel_name="hr.employee", string='Implemented By')
    request_start_datetime = fields.Datetime(string='RC Request Start Date & Time')
    resolution_date_time = fields.Datetime(string='RC Resolution Date & Time')
    total_duration = fields.Float(string='TOTAL DURATION (H:M)', compute='compute_time_difference')

    additional_info = fields.Char(string='Additional Information')

    #invoice
    invoices_count = fields.Integer(string="Invoices", compute="count_invoices")

    #Approvals
    finance_manager_id = fields.Many2one(comodel_name="res.users", string='Finanace Manager', readonly=True)
    finance_approval_date = fields.Date(string='Finanace Approval Date', readonly=True)

    data_centre_manager_id = fields.Many2one(comodel_name="res.users", string='Data Centre Manager', readonly=True)
    data_centre_approval_date = fields.Date(string='Data Centre Approval Date', readonly=True)

    service_delivery_manager_id = fields.Many2one(comodel_name="res.users", string='Service Delivery Manager', readonly=True)
    service_delivery_approval_date = fields.Date(string='Service Delivery Manager Approval Date', readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('remote.hand') or '/'
        res = super(RemoteHand, self).create(vals)
        res.action_alert_manager()
        return res 
    
    #alerts cc
    def action_alert_manager(self):
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_ccm')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "A new Remote Hand Request '{}' with reference '{}', needs review".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def count_invoices(self):
        invoice_obj = self.env['account.move']
        for invoice in self:
            domain = [('remote_hand_id', '=', invoice.id)]
            invoice_obj_ids = invoice_obj.search(domain)
            browseed_ids = invoice_obj.browse(invoice_obj_ids)
            invoice_obj_count = 0
            for id in browseed_ids:
                invoice_obj_count+=1
            invoice.invoices_count= invoice_obj_count
        return True

    def action_view_invoices(self):
        invoice = self.env['account.move'].search([('remote_hand_id', '=', self.id)])
        action = self.env.ref('account.action_move_out_invoice_type')
        result = action.read()[0]
        if self.invoices_count != 1:
            result['domain'] = "[('id', 'in', " + str(invoice.ids) + ")]"
        elif self.invoices_count == 1:
            res = self.env.ref('account.view_move_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = invoice.id
        return result

    def compute_time_difference(self):
        for date in self:
            if date.resolution_date_time and date.request_start_datetime:
                time_diff = fields.Datetime.from_string(date.resolution_date_time) - fields.Datetime.from_string(date.request_start_datetime)
                date.total_duration = float(time_diff.days) * 24 + (float(time_diff.seconds) / 3600)
            else:
                date.total_duration = 0

    #submit to finance
    def button_submit(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('account.group_account_manager')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Remote Hand Request for '{}', needs approval".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to Data Centre
    def button_finance_approve(self):
        if self.partner_id.remote_hands_count > self.partner_id.free_remote_hands and self.invoices_count == 0:
            raise UserError("This client no longer has free remote hands, Hence an invoice should be raised! ")

        self.write({'state': 'finance_approved'})
        self.finance_manager_id = self.env.uid
        self.finance_approval_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_dc')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Remote Hand Request for '{}', has been approved by Finance and needs your approval".format(self.ref)
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
        subject = "Remote Hand Request for '{}', has been approved by Data Centre and needs you to begin implementaton".format(self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approved by Service Delivery
    def button_approve(self):
        self.write({'state': 'approved'})
        self.service_delivery_manager_id = self.env.uid
        self.service_delivery_approval_date = date.today()
        subject = "Remote Hand Request for '{}', has been Approved by Service Delivery".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Remote Hand Request for '{}', has been rejected".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

    #To create invoice
    def create_invoice(self):
        """
        Method to open create invoice form
        """

        view_ref = self.env['ir.model.data'].get_object_reference('account', 'view_move_form')
        view_id = view_ref[1] if view_ref else False
         
        res = {
            'type': 'ir.actions.act_window',
            'name': ('Customer Invoice'),
            'res_model': 'account.move',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'context': {
                'default_partner_id': self.partner_id.id, 
                'default_remote_hand_id': self.id, 
                'default_move_type': 'out_invoice',
                }
        }
        
        return res