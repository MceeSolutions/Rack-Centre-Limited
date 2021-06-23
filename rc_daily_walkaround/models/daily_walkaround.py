# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DailyWalkaround(models.Model):
    _name = 'rc_daily_walkaround.walkaround'
    _description = 'Walkaround'
    
    name = fields.Char(string="Section")
    date = fields.Date(string="Date")
    input_ids = fields.One2many(comodel_name='rc_daily_walkaround.walkaround.input', inverse_name="walkaround_id", string="Inputs")


class DailyWalkaroundInput(models.Model):
    _name = 'rc_daily_walkaround.walkaround.input'
    _description = 'Walkaround Input'
    
    name = fields.Char(string="Section")
    section_id = fields.Many2one(comodel_name="rc_daily_walkaround.walkaround.section", string="Section")
    question_id = fields.Many2one(comodel_name="rc_daily_walkaround.walkaround.question", string="Task")
    answer_id = fields.Many2one(comodel_name="rc_daily_walkaround.walkaround.answer", string="Status")
    comment = fields.Text(string="Comments")
    walkaround_id = fields.Many2one(comodel_name="rc_daily_walkaround.walkaround", string="Walkaround")


class DailyWalkaroundSection(models.Model):
    _name = 'rc_daily_walkaround.walkaround.section'
    _description = 'Walkaround Section'
    
    name = fields.Char(string="Section")


class DailyWalkaroundQuestion(models.Model):
    _name = 'rc_daily_walkaround.walkaround.question'
    _description = 'Walkaround Question'
    
    name = fields.Char(string="Task")


class DailyWalkaroundAnswer(models.Model):

    _name = 'rc_daily_walkaround.walkaround.answer'
    _description = 'Status of Equipments'

    name = fields.Char(string="Status")
