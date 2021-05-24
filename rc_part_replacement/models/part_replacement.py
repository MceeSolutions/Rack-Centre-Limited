# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartReplacement(models.Model):
    _name = 'rc_part_replacement.part_replacement'
    _description = 'Part Replacement'
    _inherit = 'mail.thread'

    name = fields.Char(string="Description...",)
    user_id = fields.Many2one(comodel_name="res.users", string="Requested by")
    date_request = fields.Date(string="Requested On")
    description = fields.Text(string="Additional Note")
    asset_id = fields.Many2one(comodel_name="account.asset.asset")
    state = fields.Selection(selection=[
        ('draft', 'New'),
        ('open', "Submitted"),
        ('validate', "Validated"),
        ('approve', "Approved"),
        ('reject', "Rejected"),
        ('cancel', "Cancelled"),
    ], string="State", default="draft", readonly=True)
    line_ids = fields.One2many(comodel_name="rc_part_replacement.part_replacement.line", inverse_name="replacement_id", string="Fault Description")

    def submit(self):
        self.state = 'open'

    def validate(self):
        self.state = 'approve'

    def approve(self):
        self.state = 'approve'

    def reject(self):
        self.state = 'reject'

    def cancel(self):
        self.state = 'cancel'

    def reject_to_draft(self):
        self.state = 'draft'


class PartReplacementLine(models.Model):
    _name = 'rc_part_replacement.part_replacement.line'
    _description = 'Part Replacement Line'

    product_id = fields.Many2one(comodel_name="product.product", string="Damaged Part")
    fault = fields.Char(string="Identified Fault")
    date_request = fields.Date(related="replacement_id.date_request")
    replacement_id = fields.Many2one(comodel_name="rc_part_replacement.part_replacement", string="Replacement")
    state = fields.Selection(related="replacement_id.state")