#-*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectSchedule(models.Model):
    _name = 'project.schedule'
    _description = 'Project Schedule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id','=', self.env.uid)])

    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('approved', 'Project Schedule Approved'),
        ('resource_assigned', 'Resource Assigned'),
        ('reject', 'Project Schedule Rejected'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    name = fields.Char('Name', required=True)
    project_id = fields.Many2one(comodel_name='project.project', string="Project", required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', required=True, string='Employee', tracking=True, default=_default_employee, readonly=True, states={'draft': [('readonly', False)]})
    project_team_ids = fields.Many2many(comodel_name='hr.employee', string="Team Members")
    schedule_line_ids = fields.One2many(comodel_name='project.schedule.line', inverse_name='schedule_id', string="Schedule Lines", copy=True, readonly=True, states={'draft': [('readonly', False)]})

    #submit to elt manager
    def button_submit(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_project.group_psa')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Project Schedule '{}', from {} needs approval".format(self.name, self.employee_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approved'})
        subject = "Project Schedule '{}', from {} has been Approved".format(self.name, self.employee_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
        for activity_type in self.schedule_line_ids:
            date_deadline = self.env['mail.activity']._calculate_date_deadline(activity_type.activity_type_id)
            self.project_id.activity_schedule(
                activity_type_id=activity_type.activity_type_id.id,
                summary=activity_type.summary,
                note=activity_type.note,
                user_id=activity_type.responsible_id.id,
                date_deadline=activity_type.date_deadline
            )
    
    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "Project Schedule '{}', from {} has been rejected".format(self.name, self.employee_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})

class ProjectSchedule(models.Model):
    _name = 'project.schedule.line'
    _description = 'Project Schedule Lines'

    schedule_id = fields.Many2one(comodel_name='project.schedule')

    activity_type_id = fields.Many2one(
        'mail.activity.type', 'Activity Type',
        default=lambda self: self.env.ref('mail.mail_activity_data_todo'),
        domain=lambda self: ['|', ('res_model_id', '=', False), ('res_model_id', '=', self.env['ir.model']._get('project.project').id)],
        ondelete='restrict'
    )
    summary = fields.Char('Summary', compute="_compute_default_summary", store=True, readonly=False)
    responsible_id = fields.Many2one('res.users', 'Responsible Person', help='Specific responsible of activity if not linked to the employee.')
    note = fields.Char('Note')
    date_deadline = fields.Date(string='Date Deadline')

    @api.depends('activity_type_id')
    def _compute_default_summary(self):
        for plan_type in self:
            if not plan_type.summary and plan_type.activity_type_id and plan_type.activity_type_id.summary:
                plan_type.summary = plan_type.activity_type_id.summary
