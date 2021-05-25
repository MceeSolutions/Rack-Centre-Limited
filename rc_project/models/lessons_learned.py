# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api

class LessonsLearned(models.Model):
    _name = 'lessons.learned'
    _description = 'Lessons Learned'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    @api.model
    def _get_default_project(self):
        ctx = self._context
        if ctx.get('active_model') == 'project.project':
            return self.env['project.project'].browse(ctx.get('active_ids')[0]).id
    
    project_id = fields.Many2one(comodel_name='project.project', string="Project", default=_get_default_project, required=True)
    national_center = fields.Char(string='National Center', required=True)
    project_manager_id = fields.Many2one(comodel_name='res.users', string='Project Manager', related="project_id.user_id")
    project_description = fields.Html(string='Project Description', related="project_id.description")

    date_identified = fields.Date(string='Date Identified', default=date.today())
    entered_by = fields.Many2one(comodel_name='hr.employee', string="Entered By")
    name = fields.Char(string='Subject', required=True)
    situation = fields.Text(string='Situation', required=True)
    recommendations_comments = fields.Text(string='Recommendations & Comments')
    follow_up_needed = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Follow-Up Needed?', tracking=True, required=True)
