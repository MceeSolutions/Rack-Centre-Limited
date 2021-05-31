# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api

class RCAForm(models.Model):
    _name = 'rca.form'
    _description = 'RCA Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'
    
    @api.model
    def _get_default_project(self):
        ctx = self._context
        if ctx.get('active_model') == 'project.project':
            return self.env['project.project'].browse(ctx.get('active_ids')[0]).id
    
    @api.model
    def _get_default_issue(self):
        ctx = self._context
        if ctx.get('active_model') == 'issue.form':
            return self.env['issue.form'].browse(ctx.get('active_ids')[0]).id

    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id','=', self.env.uid)])
    
    state = fields.Selection([
        ('open', 'Open'),
        ('wip', 'Work in Progress'),
        ('closed', 'Closed'),
        ('late', 'Late'),
        ('on_hold', 'On Hold'),
        ('combined', 'Combined'),
        ], string='Status', readonly=False, index=True, copy=False, default='open', tracking=True)

    name = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')

    date_time = fields.Datetime(string='Date & Time', default=date.today())
    project_id = fields.Many2one(comodel_name='project.project', string="Project", default=_get_default_project, required=True)
    incident = fields.Char(string='Incident/Problem Title', required=True)
    reference = fields.Char(string='Reference ID', required=True)

    issue_id = fields.Many2one(comodel_name='issue.form', string="Reference", default=_get_default_issue, required=False)
    
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Entered By", default=_default_employee, required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Assigned To')

    description = fields.Text(string='Event Description', required=True)
    findings = fields.Text(string='Findings', required=True)
    action_taken = fields.Text(string='Action Taken', required=True)
    resolution = fields.Text(string='Resolution', required=True)
    root_cause_analysis = fields.Text(string='Root Cause Analysis', required=True)
    responder = fields.Char(string='Responder', required=True)
    investigative_team = fields.Text(string='Investigative Team', required=True)

    #Approvals
    project_manager_id = fields.Many2one(comodel_name="res.users", string='Project Manager', readonly=True)
    project_approval_date = fields.Date(string='Project Manager Approval Date', readonly=True)

    partner_id = fields.Many2one(comodel_name="res.partner", string='Project Owner', readonly=True)
    partner_id_date = fields.Date(string='Project Owner Approval Date', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('rca.form') or '/'
        return super(RCAForm, self).create(vals)    
