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

    business_need = fields.Char(string="Business Need")

    evaluated = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ], string='Vendor(s) Evaluated?', default='no', copy=False, tracking=True)

    justification = fields.Text(string="Justification")

    @api.model
    def create(self, vals):
        res = super(PurchaseRequisition, self).create(vals)
        res.action_launch()
        return res 

    #option to create/schedule activity
    def action_launch(self):
        if self.is_for_project:
            mail_activity_type_obj = self.env['mail.activity.type'].search([('category','=','upload_file')], limit=1)
            date_deadline = self.env['mail.activity']._calculate_date_deadline(mail_activity_type_obj)
            self.activity_schedule(
                activity_type_id=mail_activity_type_obj.id,
                summary='Upload Work Scope Document & Other relating Documents for RFP',
                user_id=self.env.uid,
                date_deadline=date_deadline
            )
    
    def vendor_valuated(self):
        self.evaluated = 'yes'
        mail_activity_type_obj = self.env['mail.activity.type'].search([('category','=','upload_file')], limit=1)
        date_deadline = self.env['mail.activity']._calculate_date_deadline(mail_activity_type_obj)
        self.activity_schedule(
            activity_type_id=mail_activity_type_obj.id,
            summary='Upload Upload Evaluation Form & Other relating Documents for This RFP',
            user_id=self.env.uid,
            date_deadline=date_deadline
        )

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
                'default_purchase_requisition_id': self.id, 
                'default_project_id': self.project_id.id, 
                }
        }
        
        return res

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

    def open_pof(self):
        pof = self.env['po.approval.request'].search([('purchase_requisition_id', '=', self.id)])
        action = self.env.ref('rc_project.rc_po_approval_request_action_window')
        result = action.read()[0]
        if self.pof_log_count != 1:
            result['domain'] = "[('id', 'in', " + str(pof.ids) + ")]"
        elif self.pof_log_count == 1:
            res = self.env.ref('rc_project.rc_po_approval_request_view', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = pof.id
        return result
        
        # self.ensure_one()
        # action = self.env.ref('rc_project.rc_po_approval_request_action_window').read()[0]
        # action['domain'] = literal_eval(action['domain'])
        # action['domain'].append(('project_id', '=', self.project_id.id))
        # return action
    


