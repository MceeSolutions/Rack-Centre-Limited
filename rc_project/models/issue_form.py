# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api
from ast import literal_eval

class IssueForm(models.Model):
    _name = 'issue.form'
    _description = 'Issue Form'
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
        ('wip', 'Work in Progress'),
        ('closed', 'Closed'),
        ('late', 'Late'),
        ('on_hold', 'On Hold'),
        ('combined', 'Combined'),
        ], string='Status', readonly=False, index=True, copy=False, default='open', tracking=True)

    user_id = fields.Many2one(comodel_name='res.users', string='Assigned To')
    project_id = fields.Many2one(comodel_name='project.project', string="Project", default=_get_default_project, required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Entered By", default=_default_employee, required=True)

    name = fields.Char(string='Issue', required=True)
    description = fields.Text(string='Description', required=True)
    likelihood = fields.Text(string='Likelihood vs Impact', required=True)
    impact = fields.Char(string='Impact', required=True)
    rag = fields.Char(string='RAG', required=True)
    mitigation = fields.Text(string='Mitigation', required=True)

    ref = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='New')

    rca_log_count = fields.Integer(compute="rca_count",string="RCA's")

    @api.model
    def create(self, vals):
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('issue.form') or '/'
        return super(IssueForm, self).create(vals)

    def button_wip(self):
        self.write({'state': 'wip'})
        subject = "Issue '{}', for {} is in Progress".format(self.name, self.project_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_closed(self):
        self.write({'state': 'closed'})
        subject = "Issue '{}', for {} has been closed".format(self.name, self.project_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def rca_count(self):
        rca_form_obj = self.env['rca.form']
        for rca_form in self:
            domain = [('issue_id', '=', rca_form.id)]
            rca_form_obj_ids = rca_form_obj.search(domain)
            browseed_ids = rca_form_obj.browse(rca_form_obj_ids)
            rca_form_obj_count = 0
            for id in browseed_ids:
                rca_form_obj_count+=1
            rca_form.rca_log_count = rca_form_obj_count
        return True

    def open_rca_log(self):
        self.ensure_one()
        action = self.env.ref('rc_project.rc_rca_form_action_window').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('issue_id', '=', self.id))
        return action

    def create_rca(self):
        """
        Method to open create RCA form
        """

        view_ref = self.env['ir.model.data'].get_object_reference('rc_project', 'rc_rca_form_view')
        view_id = view_ref[1] if view_ref else False
        
        res = {
            'type': 'ir.actions.act_window',
            'name': ('RCA FORM'),
            'res_model': 'rca.form',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'context': {
                        'default_project_id': self.project_id.id, 
                        'default_incident': self.name, 
                        'default_issue_id': self.id,
                        'default_reference': self.ref,
                        }
        }
        return res