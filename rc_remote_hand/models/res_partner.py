# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    free_remote_hands = fields.Float(string='Free Remote Hands(Mins)')

    remote_hands_count = fields.Integer(string='Remote Hands', compute="count_remote_hands")

    def count_remote_hands(self):
        remote_hand_obj = self.env['remote.hand']
        for remote in self:
            domain = [('partner_id', '=', remote.id)]
            remote_hand_obj_ids = remote_hand_obj.search(domain)
            browseed_ids = remote_hand_obj.browse(remote_hand_obj_ids)
            remote_hand_obj_count = 0
            for id in browseed_ids:
                remote_hand_obj_count+=1
            remote.remote_hands_count = remote_hand_obj_count
        return True

    def action_view_remote_hands(self):
        remote_hand = self.env['remote.hand'].search([('partner_id', '=', self.id)])
        action = self.env.ref('rc_remote_hand.rc_remote_hand_action_window')
        result = action.read()[0]
        result['domain'] = "[('id', 'in', " + str(remote_hand.ids) + ")]"
        # if self.remote_hands_count != 1:
        #     result['domain'] = "[('id', 'in', " + str(remote_hand.ids) + ")]"
        # elif self.remote_hands_count == 1:
        #     res = self.env.ref('rc_remote_hand.rc_remote_hand_view', False)
        #     result['views'] = [(res and res.id or False, 'form')]
        #     result['res_id'] = remote_hand.id
        return result