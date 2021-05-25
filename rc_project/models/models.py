#-*- coding: utf-8 -*-

from odoo import models, fields, api
from ast import literal_eval

class Project(models.Model):
    _name = "project.project"
    _inherit = ['project.project', 'mail.thread', 'mail.activity.mixin', 'rating.mixin']
    _description = "Project"

    state = fields.Selection([
        ('draft', 'New'),
        ('start', 'Commenced'),
        ('approved', 'Approved'),
        ], string='Status', default='draft', readonly=False, index=True, copy=False, tracking=True)
    
    project_team_ids = fields.Many2many(comodel_name='hr.employee', string="Team Members")

    business_case_id = fields.Many2one(comodel_name='business.case', string="Business Case")

    lessons_learned_count = fields.Integer(compute="lessons_count",string="Lessons Learned")
    change_log_count = fields.Integer(compute="change_count",string="Change Management")
    risk_identification_count = fields.Integer(compute="risk_count",string="Risk Identification")
    issue_log_count = fields.Integer(compute="issue_count",string="Issue Log")
    rfp_log_count = fields.Integer(compute="rfp_count",string="RFP's")
    wp_log_count = fields.Integer(compute="wp_count",string="WP's")

    @api.model
    def create(self, vals):
        res = super(Project, self).create(vals)
        res.action_launch()
        return res 
    
    #option to create/schedule activity
    def action_launch(self):
        mail_activity_type_obj = self.env['mail.activity.type'].search([('category','=','upload_file')], limit=1)
        date_deadline = self.env['mail.activity']._calculate_date_deadline(mail_activity_type_obj)
        self.activity_schedule(
            activity_type_id=mail_activity_type_obj.id,
            summary='Upload Initiation Document for ' + self.name,
            user_id=self.user_id.id,
            date_deadline=date_deadline
        )
        if self.business_case_id:
            self.business_case_id.write({'project_ids': [(4, self.id)] })    
    
    def name_get(self):
        res = []
        for project in self:
            result = project.name
            if project.business_case_id.name:
                result = str(project.business_case_id.name) + " " + "-" + " " + str(project.name)
            res.append((project.id, result))
        return res
    
    def commence_project(self):
        self.state = 'start'
    
    def approve_project(self):
        self.state = 'approved'

    def lessons_count(self):
        lessons_learned_obj = self.env['lessons.learned']
        for lessons_learned in self:
            domain = [('project_id', '=', lessons_learned.id)]
            lessons_learned_obj_ids = lessons_learned_obj.search(domain)
            browseed_ids = lessons_learned_obj.browse(lessons_learned_obj_ids)
            lessons_learned_obj_count = 0
            for id in browseed_ids:
                lessons_learned_obj_count+=1
            lessons_learned.lessons_learned_count = lessons_learned_obj_count
        return True

    def open_lessons_learned(self):
        self.ensure_one()
        # if self.lessons_learned_count == 1:
        #     action = self.env.ref('rc_project.rc_lessons_learned_view', False).read()[0]
        # else:
        action = self.env.ref('rc_project.rc_lessons_learned_action_window').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('project_id', '=', self.id))
        return action

    def change_count(self):
        change_log_obj = self.env['change.management']
        for change_log in self:
            domain = [('project_id', '=', change_log.id)]
            change_log_obj_ids = change_log_obj.search(domain)
            browseed_ids = change_log_obj.browse(change_log_obj_ids)
            change_log_obj_count = 0
            for id in browseed_ids:
                change_log_obj_count+=1
            change_log.change_log_count = change_log_obj_count
        return True

    def open_change_log(self):
        self.ensure_one()
        action = self.env.ref('rc_project.rc_change_management_action_window').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('project_id', '=', self.id))
        return action

    def risk_count(self):
        risk_identification_obj = self.env['risk.identification']
        for risk_identification in self:
            domain = [('project_id', '=', risk_identification.id)]
            risk_identification_obj_ids = risk_identification_obj.search(domain)
            browseed_ids = risk_identification_obj.browse(risk_identification_obj_ids)
            risk_identification_obj_count = 0
            for id in browseed_ids:
                risk_identification_obj_count+=1
            risk_identification.risk_identification_count = risk_identification_obj_count
        return True

    def open_risk_identification_log(self):
        self.ensure_one()
        action = self.env.ref('rc_project.rc_risk_identification_action_window').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('project_id', '=', self.id))
        return action

    def issue_count(self):
        issue_form_obj = self.env['issue.form']
        for issue_form in self:
            domain = [('project_id', '=', issue_form.id)]
            issue_form_obj_ids = issue_form_obj.search(domain)
            browseed_ids = issue_form_obj.browse(issue_form_obj_ids)
            issue_form_obj_count = 0
            for id in browseed_ids:
                issue_form_obj_count+=1
            issue_form.issue_log_count = issue_form_obj_count
        return True

    def open_issue_log(self):
        self.ensure_one()
        action = self.env.ref('rc_project.rc_issue_form_action_window').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('project_id', '=', self.id))
        return action

    def rfp_count(self):
        rfp_obj = self.env['purchase.requisition']
        for rfp in self:
            domain = [('project_id', '=', rfp.id)]
            rfp_obj_ids = rfp_obj.search(domain)
            browseed_ids = rfp_obj.browse(rfp_obj_ids)
            rfp_obj_count = 0
            for id in browseed_ids:
                rfp_obj_count+=1
            rfp.rfp_log_count= rfp_obj_count
        return True

    def open_rfp(self):
        self.ensure_one()
        action = self.env.ref('rc_project.rc_action_purchase_requisition').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('project_id', '=', self.id))
        return action

    def wp_count(self):
        wp_obj = self.env['work.package']
        for wp in self:
            domain = [('project_id', '=', wp.id)]
            wp_obj_ids = wp_obj.search(domain)
            browseed_ids = wp_obj.browse(wp_obj_ids)
            wp_obj_count = 0
            for id in browseed_ids:
                wp_obj_count+=1
            wp.wp_log_count= wp_obj_count
        return True

    def open_wp(self):
        self.ensure_one()
        action = self.env.ref('rc_project.rc_work_package_action_window').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('project_id', '=', self.id))
        return action

    #to create purchase agreement
    def create_purchase_agreement(self):
        """
        Method to open create purchase agreement form
        """

        view_ref = self.env['ir.model.data'].get_object_reference('purchase_requisition', 'view_purchase_requisition_form')
        view_id = view_ref[1] if view_ref else False
         
        res = {
            'type': 'ir.actions.act_window',
            'name': ('Purchase Agreement'),
            'res_model': 'purchase.requisition',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'context': {
                'default_project_id': self.id, 
                'default_is_for_project': True,
                }
        }
        
        return res
    
    #to create WBS
    def create_wbs(self):
        """
        Method to open create purchase agreement form
        """

        view_ref = self.env['ir.model.data'].get_object_reference('project', 'view_task_form2')
        view_id = view_ref[1] if view_ref else False
         
        res = {
            'type': 'ir.actions.act_window',
            'name': ('WBS'),
            'res_model': 'project.task',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'context': {
                'default_name': self.name + ': WBS',
                'default_project_id': self.id, 
                'default_wbs': True,
                'default_wbs_state': 'draft',
                }
        }
        
        return res

class Task(models.Model):
    _inherit = "project.task"

    wbs_state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'WBS Submitted'),
        ('approved', 'WBS Approved'),
        ], string='WBS Status', readonly=False, index=True, copy=False, tracking=True)

    wbs = fields.Boolean(string="wbs?")

    #submit wbs
    def button_submit_wbs(self):
        self.write({'wbs_state': 'submit'})
        group_id = self.env['ir.model.data'].xmlid_to_object('rc_project.group_pmo_manager')
        partner_ids = []
        for user in group_id.users:
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "WBS '{}', from {} needs your approval".format(self.name, self.user_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    def button_approve_wbs(self):
        self.write({'wbs_state': 'approved'})
        subject = "WBS '{}', from {} has been Approved".format(self.name, self.user_id.name)
        partner_ids = []
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
