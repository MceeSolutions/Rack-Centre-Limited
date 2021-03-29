# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rc_business_dev(models.Model):
#     _name = 'rc_business_dev.rc_business_dev'
#     _description = 'rc_business_dev.rc_business_dev'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
