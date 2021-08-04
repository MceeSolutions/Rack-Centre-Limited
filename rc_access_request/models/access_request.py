# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime

class AccessRequest(models.Model):
    _name = 'access.request'
    _description = 'Access Request'
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
        ('approved', 'Approved'),
        ('reject', 'Rejected'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    ref = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Company', domain=[('company_type', '=', 'company')])
    company_name = fields.Char(string='Organization')
    designation = fields.Char(string='Designation')
    purpose = fields.Selection([
        ('operational', 'Operational'),
        ('meeting', 'Meeting'),
        ('tour_access', 'Tour Access'),
        ('other', 'Others'),
        ],string='Purpose')
    access_category_id = fields.Many2one(comodel_name='access.category', string='Access Category')

    #Areas to be accessed
    office_building = fields.Boolean(string='Office Building')
    data_centre = fields.Boolean(string='Data Centre')
    dx_unit = fields.Boolean(string='DX Unit')
    dc_surroundings = fields.Boolean(string='DC Surroundings - RF shelter, teleport area, water chamber, etc.')
    staging_area = fields.Boolean(string='Staging Area')
    diesel_generator_area = fields.Boolean(string='Diesel & Generator Area')
    bcp_building = fields.Boolean(string='BCP Building')

    #Request Duration
    start_date = fields.Datetime(string='Start Date & Time')
    end_date = fields.Datetime(string='End Date & Time')

    additional_info = fields.Text(string='Additional Information')

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', tracking=True, default=_default_employee, readonly=True, states={'draft': [('readonly', False)]})
    department_id = fields.Many2one(comodel_name='hr.department', string='Department', default=_default_department)
    user_id = fields.Many2one(comodel_name="res.users", string='Requested By', default=_default_user) 
    requested_for_id = fields.Many2one(comodel_name="res.partner", string='Requested for')
    request_date = fields.Date(string='Request Date', default=date.today())

    #Approvals
    approver_id = fields.Many2one(comodel_name="res.users", string='Approved By', readonly=True)
    approver_date = fields.Date(string='Approved Date', readonly=True)

    access_request_line_ids = fields.One2many('access.request.lines', 'access_request_id', string="Visitors", ondelete='cascade', copy=True)

    @api.model
    def create(self, vals):
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('access.request') or '/'
        res = super(AccessRequest, self).create(vals)
        res.action_alert_manager()
        return res 
    
    #alerts cc
    def action_alert_manager(self):
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_service.group_ccm')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "A new Access Request for '{}' with reference '{}', needs review".format(self.name, self.ref)
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
        subject = "Access Request for '{}' with reference '{}', needs approval".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approved'})
        self.approver_id = self.env.uid
        self.approver_date = date.today()
        subject = "Access Request for '{}' with reference '{}', has been Approved".format(self.name, self.ref)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Access Request for '{}' with reference '{}', has been rejected".format(self.name, self.ref)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

class AccessRequestLines(models.Model):
    _name = 'access.request.lines'
    _description = 'Visitors'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

    access_request_id = fields.Many2one(comodel_name="access.request", string='access request')

    #visitors
    name = fields.Char(string='Visitor Name')
    designation = fields.Char(string='Visitor Designation')
    company = fields.Char(string='Visitor Company')
    phone = fields.Char(string='Visitor Phone No.')

    start_date = fields.Datetime(string='Start Date & Time', related='access_request_id.start_date')
    end_date = fields.Datetime(string='End Date & Time', related='access_request_id.end_date')

    check_in_status = fields.Selection([
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ],string='Check-In Status', tracking=True)

    checked_in = fields.Datetime(string='Check in date & time', tracking=True)
    checked_out = fields.Datetime(string='Check out date & time', tracking=True)

    def button_check_in(self):
        self.write({'check_in_status': 'checked_in'})
        self.checked_in = datetime.today()
    
    def button_check_out(self):
        self.write({'check_in_status': 'checked_out'})
        self.checked_out = datetime.today()
