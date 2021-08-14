#-*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    import_create_date = fields.Datetime('Creation Date', readonly=False, copy=False, index=True)
    import_created_by = fields.Datetime('Created By', readonly=False, copy=False, index=True)
