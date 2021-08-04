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

    creation_date = fields.Datetime(string='Creation Date', readonly=False)

    channel_partner = fields.Char(string='Channel Partner')
    source_url = fields.Char(string='Source URL')
    lead_source = fields.Char(string='Lead Source')
    lead_status = fields.Char(string='Lead Status')
    linkedin_connection_by_sales_team = fields.Char(string='LinkedIn Connection by Sales Team')
    leads_to_pipeline_conversion = fields.Char(string='Leads to Pipeline Conversion')

    def _get_default_contact_name(self):
        self.contact_name = self.last_name + self.first_name