# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JobCompletion(models.Model):
    _name = 'rc_job_completion.job_completion'
    _description = 'Job Completion'
    _inherit = 'mail.thread'
    
    def _get_session_user(self):
            return self._uid

    name = fields.Char(string="Describe the job done", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Contractor", required=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Employee", default=_get_session_user, required=True)
    description = fields.Text(string="Summary of the work that was done")
    signed_form = fields.Binary(string="Signed Form", readonly=True, states={'submit': [('readonly', False)]})
    state = fields.Selection(selection=[
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
    ], string="State", default="draft")
    line_ids = fields.One2many(comodel_name="rc_job_completion.job_completion.line", inverse_name="job_completion_id", string="Job Details")

    def submit(self):
        self.state = 'submit'
    
    def reject(self):
        self.state = 'reject'

    def validate(self):
        self.state = 'approve'

class JobCompletion(models.Model):
    _name = 'rc_job_completion.job_completion.line'
    _description = 'Tasks'

    name = fields.Char(string="Describe the job done")
    description = fields.Text(string="Summary of the work that was done")
    job_completion_id = fields.Many2one(comodel_name="rc_job_completion.job_completion", string="Job completion Form")