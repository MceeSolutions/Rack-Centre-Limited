from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_discount_limit = fields.Float("Sales Discount Limit", config_parameter='rc_business_dev.discount_limit')