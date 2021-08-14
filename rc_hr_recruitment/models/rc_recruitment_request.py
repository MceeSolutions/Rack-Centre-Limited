# -*- coding: utf-8 -*-

import datetime
from datetime import date, timedelta

from odoo import models, fields, api


class RecruitmentRequest(models.Model):
    _name = 'recruitment.request'
    _description = 'Recruitment Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    def _default_department(self):
        employee =  self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee.department_id
    
    state = fields.Selection([('draft', 'New'),
                              ('submit', 'Submitted'),
                              ('approve', 'Approved'),
                              ('reject', 'Rejected'),
                              ('cancel', 'Cancel')
                              ], string='Status', index=True, readonly=False, tracking=True, copy=False, default='draft', required=True,
                              help='Recruitment Request State')

    #DEPARTMENT
    name = fields.Char(string='Request', tracking=True, required=True, copy=False)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Requesting Employee', required=True, tracking=True, default=_default_employee)
    request_date = fields.Date(string='Date of Request', default=date.today(), required=True, tracking=True)
    department_id = fields.Many2one(comodel_name='hr.department', string='Department', required=True, default=_default_department, tracking=True)

    #POSITION
    type = fields.Selection([('full_time', 'Full-Time'), ('part_time', 'Part-Time')], string='Type', tracking=True, default='full_time', required=True)
    category = fields.Selection([('exempt', 'Exempt'), ('non_exempt', 'Non-Exempt')], string='Category', tracking=True, default='exempt', required=True)
    job_title = fields.Char(string='Job Title')
    reason_for_hire = fields.Selection([('new', 'New'), ('replacement', 'Replacement')], string='Reason for Hire', tracking=True, default='replacement', required=True)
    replacing_employee_id = fields.Many2one(comodel_name='hr.employee', string='Replacing Employee (Name)', tracking=True, copy=False)
    reason = fields.Text(string='Reason')
    position_description = fields.Text(string='Position Description')
    preferred_start_date = fields.Date(string='Preferred Start Date')
    grade_position = fields.Float(string='Grade Position')

    existing_job_position = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Existing Job Position?', tracking=True, default='no', required=True)
    job_id = fields.Many2one(comodel_name='hr.job', string='Job Position', tracking=True)

    #APPROVALS
    hr_manager_approval = fields.Many2one(comodel_name='res.users', string='Hiring Manager', readonly=True, tracking=True, copy=False)
    hr_manager_approval_date = fields.Date(string='Hiring Manager Approval Date', readonly=True, tracking=True, copy=False)

    finance_director_approval = fields.Many2one(comodel_name='res.users', string='Finance Director', readonly=True, tracking=True, copy=False)
    finance_director_approval_date = fields.Date(string='Finance Director Approval Date', readonly=True, tracking=True, copy=False)

    #onchange actions
    @api.onchange('job_id')
    def job_id_change(self):
        if self.job_id:
            self.job_title = self.job_id.name
            self.position_description = self.job_id.description

    @api.onchange('reason_for_hire')
    def reason_for_hire_change(self):
        if self.reason_for_hire == 'new':
            self.replacing_employee_id = False

    @api.onchange('existing_job_position')
    def existing_job_position_change(self):
        if self.existing_job_position == 'no':
            self.job_id = False

    @api.onchange('employee_id')
    def employee_id_change(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id
            
    #submit to line manager
    def button_submit(self):
        self.write({'state': 'submit'})
        partner_ids = []
        if self.employee_id.parent_id.user_id:
            partner_ids.append(self.employee_id.parent_id.user_id.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Recruitment Request '{}', from {} needs approval".format(self.name, self.employee_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approve'})
        group_id = self.env['ir.model.data'].xmlid_to_object('hr.group_hr_user')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Recruitment Request '{}', from {} has been approved by supervisor".format(self.name, self.employee_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Recruitment Request '{}', from {} has been rejected".format(self.name, self.employee_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

    #option to create new job positions
    def create_job_position(self):        
        if self.existing_job_position == 'no':            
            vals={                
            'name': self.job_title,
            'department_id': self.department_id.id,                        
            }            
        job_obj = self.env['hr.job']
        self.job_id = job_obj.create(vals)
        self.existing_job_position = 'yes'
