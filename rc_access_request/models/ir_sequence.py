from odoo import models, fields, api, _


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    def _check_request_sequence(self):
        request_code = self.env['ir.model.data'].xmlid_to_object('rc_access_request.seq_access_request')
        if request_code:
            request_code.number_next_actual = 1
