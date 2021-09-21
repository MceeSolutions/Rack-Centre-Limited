#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    priority = fields.Selection(selection_add=[('4', "Critical priority")])

    ref = fields.Char(string='Incident ID', copy=False, default='Nil')
    impact = fields.Selection([('1', '1-Extensive/Widespread'),('2', '2-Significant/Large'),('3', '3-Moderate/Limited'),('4', '4-Minor/Localized')], string='Impact', tracking=True)
    service_target = fields.Selection([('within', 'Within the Service Target'),('breached', 'Service Targets Breached')], string='SLM Real Time Status')
    resolution = fields.Text(string='Resolution')

    incident_time = fields.Datetime(string='Incident Date & Time')
    
    incident_summary = fields.Selection([
        ('Resolved within SLA', 'Resolved within SLA'),
        ('Resolved outside SLA', 'Resolved outside SLA'),
        ], string='Incident Summary', copy=False)

    @api.model
    def create(self, vals):
        if vals.get('ref', 'Nil') == 'Nil':
            vals['ref'] = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or '/'
        res = super(HelpdeskTicket, self).create(vals)
        return res 

class HelpdeskSLA(models.Model):
    _inherit = 'helpdesk.sla'

    priority = fields.Selection(selection_add=[('4', "Critical priority"), ], ondelete={'4': 'set default'})