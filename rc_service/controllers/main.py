# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from werkzeug.utils import redirect

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError

class CommandCentre(http.Controller):
    @http.route('/download_project_implementation_plans', type="http", auth='user', website=True)
    def download_project_implementation_plan(self, **kw):
        project_implementation_plan = http.request.env['ir.model.data'].sudo().xmlid_to_object('rc_service.documents_commnand_centre_project_implementation_plan')
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(project_implementation_plan.attachment_id.id))],
            ["name", "datas", "type", "res_model", "res_id", "type", "url"]
        )
        if attachment:
            attachment = attachment[0]
        
        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = BytesIO(base64.standard_b64decode(attachment["datas"]))
            return http.send_file(data, filename=attachment['name'], as_attachment=True)
        else:
            return request.not_found()
    
    @http.route('/download_rack_topology_planning_form', type="http", auth='user', website=True)
    def download_rack_topology_planning_form(self, **kw):
        rack_topology_planning_form = http.request.env['ir.model.data'].xmlid_to_object('rc_service.documents_commnand_centre_rack_topology_planning_form')
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(rack_topology_planning_form.attachment_id.id))],
            ["name", "datas", "type", "res_model", "res_id", "type", "url"]
        )
        if attachment:
            attachment = attachment[0]
        
        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = BytesIO(base64.standard_b64decode(attachment["datas"]))
            return http.send_file(data, filename=attachment['name'], as_attachment=True)
        else:
            return request.not_found()

    @http.route('/download_health_screening_form', type="http", auth='user', website=True)
    def download_health_screening_form(self, **kw):
        health_screening_form = http.request.env['ir.model.data'].xmlid_to_object('rc_service.documents_commnand_centre_health_screening_form')
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(health_screening_form.attachment_id.id))],
            ["name", "datas", "type", "res_model", "res_id", "type", "url"]
        )
        if attachment:
            attachment = attachment[0]
        
        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = BytesIO(base64.standard_b64decode(attachment["datas"]))
            return http.send_file(data, filename=attachment['name'], as_attachment=True)
        else:
            return request.not_found()