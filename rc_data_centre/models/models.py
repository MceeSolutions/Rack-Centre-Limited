# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rc_data_centre(models.Model):
#     _name = 'rc_data_centre.rc_data_centre'
#     _description = 'rc_data_centre.rc_data_centre'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
