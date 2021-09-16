# -*- coding: utf-8 -*-

from odoo import models, fields, api

FIXED_PAL  = 450
FIXED_CABINET  = 900

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

    deal_name = fields.Char(string='Deal Name')
    location = fields.Char(string='Location')
    next_step = fields.Char(string='Next Step')

    pal = fields.Float(string='PAL')
    cabinet = fields.Float(string='Cabinet')

    cabinet_foot_print = fields.Char(string='Cabinet Foot print')
    pal_cabinet = fields.Char(string='PAL/Cabinet')

    pal_currency = fields.Float(string='PAL $', default=450)
    cabinet_currency = fields.Float(string='Cabinet $', default=900)

    discount_cabinet = fields.Float(string='Discount/Cabinet %', compute="_compute_pal")
    discount_pal = fields.Float(string='Discount/PAL %', compute="_compute_pal")

    blended_rate = fields.Float(string='Blended Rate', compute="_compute_pal")
    revenue_date = fields.Datetime(string='Revenue Date')

    weighted_mrr = fields.Float(string='Weighted MRR', compute="_compute_pal")
    weighted_cabinet = fields.Float(string='Weighted Cabinet', compute="_compute_pal")
    weighted_pal = fields.Float(string='Weighted PAL', compute="_compute_pal")
    
    expected_revenue = fields.Monetary('Expected Revenue MRR', currency_field='company_currency', tracking=True, compute="_compute_pal")

    location = fields.Char(string='Location')
    service_type = fields.Char(string='Service Type')
    installation_charge = fields.Float(string='Installation Charge')


    def _compute_pal(self):
        for self in self:
            self.discount_cabinet = (FIXED_CABINET - self.cabinet_currency) / FIXED_CABINET * 100
            self.discount_pal = (FIXED_PAL - self.pal_currency) / FIXED_PAL * 100
            self.expected_revenue = (self.pal * self.pal_currency) + (self.cabinet * self.cabinet_currency)
            if self.expected_revenue == 0:
                self.blended_rate = 0
            else:
                self.blended_rate = self.expected_revenue / self.pal
            self.weighted_mrr = self.expected_revenue * (self.probability/100)
            self.weighted_cabinet = self.cabinet_currency * (self.probability/100)
            self.weighted_pal = self.pal_currency * (self.probability/100)
    
    def _get_default_contact_name(self):
        self.contact_name = self.last_name + self.first_name

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        self.probability = self.stage_id.stage_probability

class Stage(models.Model):
    _inherit = 'crm.stage'

    stage_probability = fields.Float(string='Stage Probability')

