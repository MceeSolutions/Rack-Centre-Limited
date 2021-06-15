# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    cross_connect_id = fields.Many2one(comodel_name='cross.connect', string="Cross Connect")