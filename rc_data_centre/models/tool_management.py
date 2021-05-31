from datetime import date
from odoo import models, fields


class ToolManagement(models.Model):
    _name = 'tool.management'
    _description = 'Tool Management'
    _inherit = 'mail.thread'

    def get_session_user(self):
        return self.env.uid

    name = fields.Char(string="Name")
    user_id = fields.Many2one(comodel_name="res.users", string="Requester", default=get_session_user)
    date_request = fields.Date(string="Date", default=date.today())
    approver = fields.Many2one(comodel_name="res.users", string="Approved By")
    date_approve = fields.Date(string="Approval Date")
    state = fields.Selection(selection=[
        ('draft', "New"),
        ('submit', "Confirmed"),
        ('approve', "Approved"),
        ('reject', "Rejected"),
        ('cancel', "Cancelled"),
    ], string="State", default="draft", tracking=True)
    line_ids = fields.One2many(comodel_name="tool.management.line", inverse_name="management_id", string="Tools")

    def submit(self):
        self.state = 'submit'

    def approve(self):
        self.state = 'approve'
    
    def reject(self):
        self.state = 'reject'

    def cancel(self):
        self.state = 'cancel'
    
    def reset_to_draft(self):
        self.state = 'draft'


class ToolManagementLine(models.Model):
    _name = 'tool.management.line'
    _description = 'Tool Management Line'

    tool_id = fields.Many2one(comodel_name='tool.tool', string="Tool")
    qty_request = fields.Float(string="Quantity")
    qty_done = fields.Float(string="Done")
    management_id = fields.Many2one(comodel_name="tool.management", string="Management")


class ToolTool(models.Model):
    _inherit = 'mail.thread'
    _name = 'tool.tool'
    _description = 'Tools'
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
