# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccessCategory(models.Model):
    _name = 'access.category'
    _description = 'Access Category'
    _order = 'create_date DESC'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)