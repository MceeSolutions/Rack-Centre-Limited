# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SocialPost(models.Model):
    _inherit = 'social.post'

    def _get_website_contactus(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        contactus_url = base_url + '/contactus'
        return contactus_url

    message = fields.Text("Message", required=True, default=_get_website_contactus)
