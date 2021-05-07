# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api

class ChangeManagement(models.Model):
    _name = 'change.management'
    _description = 'Change Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    @api.model
    def _get_default_project(self):
        ctx = self._context
        if ctx.get('active_model') == 'project.project':
            return self.env['project.project'].browse(ctx.get('active_ids')[0]).id
    
    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id','=', self.env.uid)])

    state = fields.Selection([
        ('open', 'Open'),
        ('submit', 'Submit'),
        ('approved', 'PSC Approved'),
        ('reject', 'PSC Rejected'),
        ('wip', 'Work in Progress'),
        ('closed', 'Closed'),
        ('late', 'Late'),
        ('on_hold', 'On Hold'),
        ('combined', 'Combined'),
        ], string='Current Status', readonly=False, index=True, copy=False, default='open', tracking=True)
    
    priority = fields.Selection([
        ('nil', 'None'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
        ], string='Priority', readonly=False, index=True, copy=False, default='low', tracking=True)

    description = fields.Char(string='Change Request Description', required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Assigned To')
    expected_resolution_date = fields.Date(string='Expected Resolution Date', default=date.today())
    escalation_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Escalation Required?', tracking=True, required=True)
    action_steps = fields.Text(string='Action Steps')
    impact_summary = fields.Char(string='Impact Summary')
    change_request_type = fields.Selection([('product', 'Product'), ('project', 'Project'), ('other', 'Other')], string='Change Request Type', tracking=True, required=True)
    resolution_date = fields.Date(string='Actual Resolution Date', default=date.today())

    project_id = fields.Many2one(comodel_name='project.project', string="Project", default=_get_default_project, required=True)
    national_center = fields.Char(string='National Center', required=True)
    project_manager_id = fields.Many2one(comodel_name='res.users', string='Project Manager', related="project_id.user_id")
    project_description = fields.Html(string='Project Description', related="project_id.description")

    date_identified = fields.Date(string='Date Identified', default=date.today())
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Entered By", default=_default_employee, required=True)

    resolution_rationale = fields.Text(string='Final Resolution & Rationale')

    def button_submit_change(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_project.group_pmo_manager','rc_project.group_psc')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Change Request for '{}', needs review".format(self.project_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approved'})
        subject = "Change Request '{}', has been Approved".format(self.project_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Change Request '{}', has been rejected".format(self.project_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'open'})

    def button_in_progress(self):
        self.write({'state': 'wip'})
        subject = "Change Request '{}', is in Progress".format(self.project_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_closed(self):
        self.write({'state': 'closed'})
        subject = "Change Request '{}', has been closed".format(self.project_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)