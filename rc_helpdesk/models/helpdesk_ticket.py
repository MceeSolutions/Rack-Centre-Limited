#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    priority = fields.Selection(selection_add=[('4', "Critical priority")])

# class HelpdeskSLA(models.Model):
#     _inherit = 'helpdesk.sla'

#     priority = fields.Selection(selection_add=[('4', "Critical priority")], string='Minimum Priority', default='0', required=True,
#         help='Tickets under this priority will not be taken into account.')