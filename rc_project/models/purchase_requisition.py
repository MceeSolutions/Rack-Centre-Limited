#-*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.model
    def _get_default_project(self):
        ctx = self._context
        if ctx.get('active_model') == 'project.project':
            return self.env['project.project'].browse(ctx.get('active_ids')[0]).id

    project_id = fields.Many2one(comodel_name='project.project', string="Project", default=_get_default_project)
    is_for_project = fields.Boolean(string="is for project?")

    @api.onchange('project_id')
    def project_id_change(self):
        if self.project_id:
            self.is_for_project = True

