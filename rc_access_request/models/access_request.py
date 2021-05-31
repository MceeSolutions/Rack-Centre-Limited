# -*- coding: utf-8 -*-

from odoo import models, fields

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

    name = fields.Char(string='Name', required=True, copy=False, default='New')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Organization', domain=[('company_type', '=', 'company')])
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

    #submit to elt manager
    def button_submit(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_base.group_coo', 'rc_base.group_md')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Access Request for '{}', needs approval".format(self.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approved'})
        subject = "Access Request for '{}', has been Approved".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Access Request for '{}', has been rejected".format(self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

