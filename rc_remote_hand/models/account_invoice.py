# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    remote_hand_id = fields.Many2one(comodel_name='remote.hand', string="Remote Hand")