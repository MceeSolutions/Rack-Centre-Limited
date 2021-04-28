# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead(models.Model):
    _inherit = 'crm.lead'

    industry_id = fields.Many2one('res.partner.industry', string='Vertical')
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    interests = fields.Selection([
        ('colocation', 'Colocation'),
        ('cloud', 'Cloud'),
        ('remote_hands', 'Remote Hands'),
        ('free_cross_connect', 'Free Cross Connect'),
        ('peering', 'Peering'),
        ('interconnect', 'Interconnect'),
        ('request_tour', 'Request a Tour'),
        ('others', 'Others')], string='Interested in',
        copy=False, tracking=True)

    def _get_default_contact_name(self):
        self.contact_name = self.last_name + self.first_name