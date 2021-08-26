# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CoordinatorGroup(models.Model):
    _name = 'coordinator.group'
    _description = 'Co-Ordinator Group'

    name = fields.Char(string='Name', required=True)
    user_id = fields.Many2one(comodel_name="res.users", string='Manager')
    active = fields.Boolean(string='Active', default=True)
