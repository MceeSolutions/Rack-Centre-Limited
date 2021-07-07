# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime

class MaterialGatepass(models.Model):
    _name = 'material.gatepass'
    _description = 'Material Gatepass'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    def _default_user(self):
        return self.env.uid

    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id','=', self.env.uid)])
    
    def _default_department(self): # this method is to search the hr.employee and return the user id of the person clicking the form atm
        user = self.env['hr.employee'].sudo().search([('user_id','=',self.env.uid)])
        return user.department_id.id
    
    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('dc_approved', 'Data Centre Approved'),
        ('approved', 'CSO Approved'),
        ('reject', 'Rejected'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    ref = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Company', domain=[('company_type', '=', 'company')])

    name = fields.Char(string='Name', required=True)
    request_date = fields.Date(string='Date', default=date.today())
    company_name = fields.Char(string='Company')
    material_from = fields.Char(string='From')
    material_to = fields.Char(string='To')

    line_ids = fields.One2many(comodel_name="material.gatepass.line", inverse_name="gatepass_id", ondelete='cascade', string="Materials")

    #REASON FOR MOVEMENT
    summary = fields.Text(string='Summary')

    additional_info = fields.Text(string='Additional Information')

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', tracking=True, default=_default_employee, readonly=True, states={'draft': [('readonly', False)]})
    department_id = fields.Many2one(comodel_name='hr.department', string='Department', default=_default_department)
    user_id = fields.Many2one(comodel_name="res.users", string='Requested By', default=_default_user) 
    requested_for_id = fields.Many2one(comodel_name="res.partner", string='Requested for')

    #Approvals
    dc_approver_id = fields.Many2one(comodel_name="res.users", string='Data Centre Approval', readonly=True)
    dc_approver_date = fields.Date(string='Data Centre Approval Date', readonly=True)

    cso_approver_id = fields.Many2one(comodel_name="res.users", string='CSO Approval', readonly=True)
    cso_approver_date = fields.Date(string='CSO Approval Date', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('access.request') or '/'
        res = super(MaterialGatepass, self).create(vals)
        res.action_alert_manager()
        return res 
    
    #alerts cc
    def action_alert_manager(self):
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_ccm')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "A new material gatepass for '{}' with reference '{}', needs review".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #submit to elt manager
    def button_submit(self):
        self.write({'state': 'submit'}) 
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_dc')
        partner_ids = []
        if self.employee_id:
            if self.employee_id.parent_id.user_id:
                partner_ids.append(self.employee_id.parent_id.user_id.partner_id.id)
        else:
            for user in group_id.users:
                partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "material gatepass for '{}' with reference '{}', needs approval".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_dc_approve(self):
        self.write({'state': 'dc_approved'}) 
        self.dc_approver_id = self.env.uid
        self.dc_approver_date = date.today()
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_dc')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "material gatepass for '{}' with reference '{}', has been approved by Data Centre needs approval".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approvals to be lnked to the appropriate group
    def button_cso_approve(self):
        self.write({'state': 'approved'})
        self.cso_approver_id = self.env.uid
        self.cso_approver_date = date.today()
        subject = "material gatepass for '{}' with reference '{}', has been Approved".format(self.name, self.ref)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "material gatepass for '{}' with reference '{}', has been rejected".format(self.name, self.ref)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})


class MaterialGatepassLine(models.Model):
    _name = 'material.gatepass.line'
    _description = 'Material Gatepass Line'

    gatepass_id = fields.Many2one(comodel_name='material.gatepass', string="material gatepass")
    description = fields.Char(string='Item Description')
    qty_request = fields.Float(string="Quantity")
    qty_done = fields.Float(string="Done")
