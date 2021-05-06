# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api

class RiskIdentification(models.Model):
    _name = 'risk.identification'
    _description = 'Risk Identification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    @api.model
    def _get_default_project(self):
        ctx = self._context
        if ctx.get('active_model') == 'project.project':
            return self.env['project.project'].browse(ctx.get('active_ids')[0]).id
    
    project_id = fields.Many2one(comodel_name='project.project', string="Project", default=_get_default_project, required=True, tracking=True)

    name = fields.Char(string='Risk', required=True)
    category = fields.Selection([
        ('cost', 'Cost'),
        ('schedule', 'Schedule'),
        ('performance', 'Performance'),
        ('legal', 'Legal'),
        ('regulatory', 'Regulatory'),
        ], string='Category', required=False,  copy=False, tracking=True)
    description = fields.Text(string='Description', required=True, tracking=True)
    impact = fields.Float(string='Impact', required=True, tracking=True)
    likelihood = fields.Float(string='Likelihood', required=True, tracking=True)
    mitigation = fields.Text(string='Mitigation', required=True, tracking=True)

    