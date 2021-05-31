# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectResource(models.TransientModel):
    _name = 'project.resource.wizard'
    _description = 'Project Resource'

    @api.model
    def _get_default_project(self):
        ctx = self._context
        if ctx.get('active_model') == 'project.project':
            return self.env['project.project'].browse(ctx.get('active_ids')[0]).id
    
    schedule_id = fields.Many2one(comodel_name='project.schedule', default=lambda self: self.env.context.get('active_id', None), required=True)

    project_id = fields.Many2one(comodel_name='project.project', string="Project", related='schedule_id.project_id', required=True)

    project_team_ids = fields.Many2many(comodel_name='hr.employee', string="Team Members")

    employee_id = fields.Many2one(
        'hr.employee', string='Employee', required=True,
        default=lambda self: self.env.context.get('active_id', None),
    )

    def action_assign(self):
        self.project_id.project_team_ids = self.project_team_ids
        self.schedule_id.write({'state': 'resource_assigned'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': self.project_id.id,
            'name': self.project_id.display_name,
            'view_mode': 'form',
            'views': [(False, "form")],
        }

    def action_launch(self):
        for activity_type in self.plan_id.plan_activity_type_ids:
            responsible = activity_type.get_responsible_id(self.employee_id)

            if self.env['hr.employee'].with_user(responsible).check_access_rights('read', raise_exception=False):
                date_deadline = self.env['mail.activity']._calculate_date_deadline(activity_type.activity_type_id)
                self.employee_id.activity_schedule(
                    activity_type_id=activity_type.activity_type_id.id,
                    summary=activity_type.summary,
                    note=activity_type.note,
                    user_id=responsible.id,
                    date_deadline=date_deadline
                )

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee',
            'res_id': self.employee_id.id,
            'name': self.employee_id.display_name,
            'view_mode': 'form',
            'views': [(False, "form")],
        }
