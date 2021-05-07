# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api

class WorkPackage(models.Model):
    _name = 'work.package'
    _description = 'Work Package'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    @api.model
    def _get_default_project(self):
        ctx = self._context
        if ctx.get('active_model') == 'project.project':
            return self.env['project.project'].browse(ctx.get('active_ids')[0]).id
    
    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id','=', self.env.uid)])
    
    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id
    
    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('approved', 'COO Approved'),
        ('reject', 'COO Rejected'),
        ('waiting', 'Awaiting Approval from PS'),
        ('ps_approved', 'PS Approved'),
        ('ps_reject', 'PS Rejected'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    name = fields.Char(string='Work Stream/Package', required=True)
    project_id = fields.Many2one(comodel_name='project.project', string="Project", default=_get_default_project, required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', required=True, string='Employee', tracking=True, default=_default_employee)
    currency_id = fields.Many2one(comodel_name='res.currency', required=True, string='Currency', default=_default_currency)

    firm = fields.Float(string='Firm')
    budgetary = fields.Float(string='Budgetary')
    estimate = fields.Float(string='Estimate')

    wp_line_ids = fields.One2many(comodel_name='work.package.line', inverse_name='wp_id', string="Package Lines")

    #submit to elt manager
    def button_submit(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_base.group_coo')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "WP '{}', for {} needs approval".format(self.name, self.project_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approved'})
        subject = "Business Case '{}', from {} has been Approved".format(self.name, self.employee_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Business Case '{}', from {} has been rejected".format(self.name, self.employee_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

    def button_submit_ps(self):
        self.write({'state': 'waiting'})
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_project.group_ps')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "WP & Budget Sheet '{}', for {} project needs sponsor approval".format(self.name, self.project_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_ps_approve(self):
        self.write({'state': 'ps_approved'})
        subject = "WP & Budget Sheet '{}', for {} has been approved".format(self.name, self.project_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
        self.action_launch()
    
    def button_ps_reject(self):
        self.write({'state': 'pms_reject'})
        subject = "WP & Budget Sheet '{}', for {} has been rejected".format(self.name, self.project_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_reset_ps(self):
        self.write({'state': 'waiting'})
    
    #option to create/schedule activity
    def action_launch(self):
        mail_activity_type_obj = self.env['mail.activity.type'].search([('category','=','upload_file')], limit=1)
        date_deadline = self.env['mail.activity']._calculate_date_deadline(mail_activity_type_obj)
        self.activity_schedule(
            activity_type_id=mail_activity_type_obj.id,
            summary='Upload Project Charter for ' + self.name,
            user_id=self.employee_id.user_id.id,
            date_deadline=date_deadline
        )

class WorkPackageLine(models.Model):
    _name = 'work.package.line'
    _description = 'Work Package Line'

    wp_id = fields.Many2one(comodel_name='work.package')

    name = fields.Char(string='Cost Item')
    initial_budget_local = fields.Float(string='Initial Budget (Local Currency)')
    initial_budget_foreign = fields.Float(string='Initial Budget ($)')
    latest_budget = fields.Float(string='Latest Budget') 
    savings = fields.Float(string='Savings', compute='compute_saving') 
    firm_up_rate = fields.Float(string='Firm-up Rate') 
    partner_id = fields.Many2one(comodel_name='res.partner', string='Vendor')
    cost_status = fields.Selection([
            ('open', 'Budgetary'),
            ('wip', 'Confirmed'),
            ('closed', 'Estimate'),
            ('late', 'Firm'),
            ('on_hold', 'Not Applicable'),
            ], string='Status')
    cost_comment = fields.Char(string='Cost Comment') 
    quote_reference = fields.Char(string='Quote Reference')

    def compute_saving(self):
        for line in self:
            line.savings = line.initial_budget_foreign - line.latest_budget

