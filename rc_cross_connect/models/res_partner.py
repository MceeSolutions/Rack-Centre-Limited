# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    free_cross_connects = fields.Integer(string='Free Cross Connects', default=1)
    cross_connect_count = fields.Integer(string='Cross Connects', compute="count_cross_connects")

    def count_cross_connects(self):
        cross_connect_obj = self.env['cross.connect']
        for connect in self:
            domain = [('partner_id', '=', connect.id)]
            cross_connect_obj_ids = cross_connect_obj.search(domain)
            browseed_ids = cross_connect_obj.browse(cross_connect_obj_ids)
            cross_connect_obj_count = 0
            for id in browseed_ids:
                cross_connect_obj_count+=1
            connect.cross_connect_count = cross_connect_obj_count
        return True

    def action_view_cross_connects(self):
        cross_connect = self.env['cross.connect'].search([('partner_id', '=', self.id)])
        action = self.env.ref('rc_cross_connect.rc_cross_connect_action_window')
        result = action.read()[0]
        result['domain'] = "[('id', 'in', " + str(cross_connect.ids) + ")]"
        # if self.remote_hands_count != 1:
        #     result['domain'] = "[('id', 'in', " + str(remote_hand.ids) + ")]"
        # elif self.remote_hands_count == 1:
        #     res = self.env.ref('rc_remote_hand.rc_remote_hand_view', False)
        #     result['views'] = [(res and res.id or False, 'form')]
        #     result['res_id'] = remote_hand.id
        return result