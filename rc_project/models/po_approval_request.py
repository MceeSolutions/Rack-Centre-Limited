# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError

class POApprovalRequest(models.Model):
    _name = 'po.approval.request'
    _description = 'PO Approval Request Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'
    
    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id','=', self.env.uid)])

    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('approved', 'Approved'),
        ('reject', 'Rejected'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

    name = fields.Char(string='Order Reference (POF NO.)', readonly=True, required=True, index=True, copy=False, default='New')
    project_id = fields.Many2one(comodel_name='project.project', string="Project", required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', required=True, string='Originator of POF(Employee)', tracking=True, default=_default_employee)
    date_raised = fields.Date(string='Date Raised', required=True)
    value_of_pof = fields.Float(string='Value of POF')
    description = fields.Text(string='Brief Description of PO', required=True)
    po_type = fields.Selection([
        ('general', 'General/Main Contractor PO'),
        ('equipment', 'Equipment PO'),
        ('other', 'Other PO/Specialist Trade Contractor PO'),
        ], string='Puchase Order Type', required=True, tracking=True)
    project_status = fields.Char(string='Project Status')

    project_manager_comment = fields.Text(string="Project's Managers COmment")
    engineering_comment = fields.Text(string='Engineering commentary')
    commercial_comment = fields.Text(string='Commercial commentary')
    other_comments = fields.Text(string='Other comments (if required)')

    schedule = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Schedule', tracking=True, default='no', required=True)
    cost = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Cost', tracking=True, default='no', required=True)
    scope = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Scope', tracking=True, default='no', required=True)
    other_atch = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Other (Minutes, Bid submission)', tracking=True, default='no', required=True)

    # pmo_manager_id = fields.Many2one(comodel_name="res.users", string='Project Management Office', readonly=True)
    # pmo_approval_date = fields.Date(string='Project Management Office Approval Date', readonly=True)

    # coo_manager_id = fields.Many2one(comodel_name="res.users", string='Chief Operations Officer', readonly=True)
    # coo_approval_date = fields.Date(string='Chief Operations Officer Approval Date', readonly=True)

    # finance_manager_id = fields.Many2one(comodel_name="res.users", string='Finance Director', readonly=True)
    # finance_approval_date = fields.Date(string='Finance Director Approval Date', readonly=True)

    purchase_requisition_id = fields.Many2one(comodel_name='purchase.requisition', string="RFP")

    psc_manager_id = fields.Many2one(comodel_name="res.users", string='PSC Manager', readonly=True)
    psc_approval_date = fields.Date(string='PSC Manager Approval Date', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('po.approval.request') or '/'
        return super(POApprovalRequest, self).create(vals)
    
    #submit to psc manager
    def button_submit(self):
        self.write({'state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_project.group_psc')
        partner_ids = []
        attachments = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "POF '{}', from {} needs approval".format(self.name, self.employee_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    #approvals to be lnked to the appropriate group
    def button_approve(self):
        self.write({'state': 'approved'})
        self.psc_manager_id = self.env.uid
        self.psc_approval_date = date.today()


        po = self.purchase_requisition_id.purchase_ids.search([('partner_id','=', self.purchase_requisition_id.vendor_id.id)], limit=1)
        po.button_confirm()

        subject = "POF '{}', from {} has been Approved".format(self.name, self.employee_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reject(self):
        self.write({'state': 'reject'})
        subject = "POF '{}', from {} has been rejected".format(self.name, self.employee_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def button_reset(self):
        self.write({'state': 'new'})