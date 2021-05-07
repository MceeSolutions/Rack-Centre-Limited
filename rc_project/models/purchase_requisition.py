#-*- coding: utf-8 -*-

from odoo import models, fields, api
from ast import literal_eval

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.model
    def _get_default_project(self):
        ctx = self._context
        if ctx.get('active_model') == 'project.project':
            return self.env['project.project'].browse(ctx.get('active_ids')[0]).id

    project_id = fields.Many2one(comodel_name='project.project', string="Project", default=_get_default_project)
    is_for_project = fields.Boolean(string="is for project?")
    pof_log_count = fields.Integer(string='POFs', compute='pof_count')

    @api.onchange('project_id')
    def project_id_change(self):
        if self.project_id:
            self.is_for_project = True
    
    #to create POF
    def create_pof(self):
        """
        Method to open create PO Approval Request Form
        """

        view_ref = self.env['ir.model.data'].get_object_reference('rc_project', 'rc_po_approval_request_view')
        view_id = view_ref[1] if view_ref else False
         
        res = {
            'type': 'ir.actions.act_window',
            'name': ('POF'),
            'res_model': 'po.approval.request',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'context': {
                # 'default_name': self.name + ': WBS',
                # 'default_wbs': True,
                # 'default_wbs_state': 'draft',
                'default_project_id': self.project_id.id, 
                }
        }
        
        return res
    
    def open_pof(self):
        self.ensure_one()
        action = self.env.ref('rc_project.rc_po_approval_request_action_window').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('project_id', '=', self.project_id.id))
        return action

    def pof_count(self):
        pof_obj = self.env['po.approval.request']
        for pof in self:
            domain = [('project_id', '=', pof.project_id.id)]
            pof_obj_ids = pof_obj.search(domain)
            browseed_ids = pof_obj.browse(pof_obj_ids)
            pof_obj_count = 0
            for id in browseed_ids:
                pof_obj_count+=1
            pof.pof_log_count= pof_obj_count
        return True
    


