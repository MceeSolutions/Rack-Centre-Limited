# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rc_hr_recruitment(models.Model):
#     _name = 'rc_hr_recruitment.rc_hr_recruitment'
#     _description = 'rc_hr_recruitment.rc_hr_recruitment'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
