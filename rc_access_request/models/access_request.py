# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccessRequest(models.Model):
    _name = 'access.request'
    _description = 'Access Request'
    _inherit = ['portal.mixin', 'mail.activity.mixin', 'mail.thread']
    _order = 'create_date DESC'

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
    purpose = fields.Char(string='Purpose')
    access_category = fields.Char(string='Access Category')

    #Areas to be accessed
    office_building = fields.Boolean(string='Office Building')
    data_centre = fields.Boolean(string='Data Centre')
    dx_unit = fields.Boolean(string='DX Unit')
    dc_surroundings = fields.Boolean(string='DC Surroundings - RF shelter, teleport area, water chamber, etc.')
    staging_area = fields.Boolean(string='Staging Area')
    diesel_generator_area = fields.Boolean(string='Diesel & Generator Area')

    #Request Duration
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    #Daily Arrival
    start_time = fields.Char(string='Start Time')
    end_time = fields.Char(string='End Time')

    additional_info = fields.Text(string='Additional Information')

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
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Access Request for '{}' with reference '{}', needs approval".format(self.name, self.ref)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approved'})
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

