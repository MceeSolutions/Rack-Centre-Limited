# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError

class BusinessCase(models.Model):
    _name = 'business.case'
    _description = 'Business Case'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'
    
    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id','=', self.env.uid)])
    
    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('approved', 'Business Case Approved'),
        ('reject', 'Business Case Rejected'),
        ('waiting', 'Awaiting Approval for PM'),
        ('pm_approved', 'PM Approved'),
        ('pm_reject', 'PM Rejected'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    name = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')
    note = fields.Text(string="Notes", readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date(string='Date', required=True, tracking=True, default=date.today(), readonly=True, states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one(comodel_name='hr.employee', required=True, string='Employee', tracking=True, default=_default_employee, readonly=True, states={'draft': [('readonly', False)]})
    
    doc_id = fields.Binary(string='Document(s)', attachment=True)

    prospective_partner_id = fields.Many2one(comodel_name="res.partner", string='Prospective Client')
    prospective_pm_id = fields.Many2one(comodel_name="res.users", string='Prospective PM')

    project_ids = fields.Many2many(comodel_name="project.project", string="Project", readonly=True)
    projects_count = fields.Integer(string="Projects", compute="count_projects")

    #Approvals
    elt_manager_id = fields.Many2one(comodel_name="res.users", string='ELT Manager', readonly=True)
    elt_approval_date = fields.Date(string='ELT Approval Date', readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('business.case') or '/'
        res = super(BusinessCase, self).create(vals)
        res.action_launch()
        return res 

    def count_projects(self):
        self.projects_count = len(self.project_ids.ids)

    def action_view_projects(self):
        action = self.env.ref('project.open_view_project_all')
        result = action.read()[0]
        if len(self.project_ids) != 1:
            result['domain'] = "[('id', 'in', " + str(self.project_ids.ids) + ")]"
        elif len(self.project_ids) == 1:
            res = self.env.ref('project.edit_project', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.project_ids.id
        return result

    #submit to elt manager
    def button_submit(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_base.group_elt')
        partner_ids = []
        attachments = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        for pdf in self.message_main_attachment_id:
            attachments.append(pdf.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Business Case '{}', from {} needs approval".format(self.name, self.employee_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids,attachment_ids=attachments)

    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approved'})
        self.elt_manager_id = self.env.uid
        self.elt_approval_date = date.today()
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

    def button_submit_prospective_pm(self):
        if not self.prospective_pm_id:
            return UserError("Please select Prospective PM!")
        
        self.write({'state': 'waiting'})
        group_id = self.env['ir.model.data'].xmlid_to_object('project.group_project_manager')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Prospestive PM '{}', from {} Business Case needs approval".format(self.prospective_pm_id.name, self.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_pm_approve(self):
        self.write({'state': 'pm_approved'})
        subject = "Prospestive PM '{}', from {} Business Case has been Approved".format(self.prospective_pm_id.name, self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_pm_reject(self):
        self.write({'state': 'pm_reject'})
        subject = "Prospestive PM '{}', from {} Business Case has been Rejected".format(self.prospective_pm_id.name, self.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_reset_pm(self):
        self.write({'state': 'waiting'})
        self.prospective_pm_id = False

    #option to create new project
    def create_project(self): 
        vals = {                
            'name': 'Project: ' + self.name,
            'user_id': self.prospective_pm_id.id,
            'partner_id': self.prospective_partner_id.id,    
            }
        project_obj = self.env['project.project'].create(vals)
        self.project_ids += project_obj

    #option to create/schedule activity
    def action_launch(self):
        mail_activity_type_obj = self.env['mail.activity.type'].search([('category','=','upload_file')], limit=1)
        date_deadline = self.env['mail.activity']._calculate_date_deadline(mail_activity_type_obj)
        self.activity_schedule(
            activity_type_id=mail_activity_type_obj.id,
            summary='Upload Business Case for' + self.name,
            user_id=self.employee_id.user_id.id,
            date_deadline=date_deadline
        )