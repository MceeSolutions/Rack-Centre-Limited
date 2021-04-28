# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError


class CashAdvance(models.Model):
    _name = 'cash.advance'
    _description = 'Cash advance Request Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'
    
    def _default_department(self): # this method is to search the hr.employee and return the user id of the person clicking the form atm
        user = self.env['hr.employee'].sudo().search([('user_id','=',self.env.uid)])
        return user.department_id.id

    def _get_user(self):
        return self.env.uid
    
    def _default_employee(self): # this method is to search the hr.employee and return the user id of the person clicking the form atm
        return self.env['hr.employee'].sudo().search([('user_id','=', self.env.uid)])
    
    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id
    
    name = fields.Char(string='Order Reference', readonly=True, required=True, index=True, default='/')
    note = fields.Char(string="Description", required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('mgr_approve', 'Line Manager Approved'),
        ('approve', 'Finance Approved'),
        ('close', 'Retired'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', track_visibility='onchange')

    date = fields.Date(string='Date', required=True, track_visibility='onchange', default=date.today(), readonly=True, states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one(comodel_name='hr.employee', required=True, readonly=True, string='Employee', track_visibility='onchange', states={'draft': [('readonly', False)]}, default=_default_employee)
    user_id = fields.Many2one(comodel_name='res.users', required=True, string='User', default=_get_user, readonly= True, states={'draft': [('readonly', False)]})
    manager_id = fields.Many2one(comodel_name="hr.employee", string="Employee Manager", compute="_get_employee_manager")
    department_id = fields.Many2one(comodel_name='hr.department', string='Department', related='employee_id.department_id', readonly=True, states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one(comodel_name='res.currency', required=True, string='Currency', default=_default_currency, readonly=True, states={'draft': [('readonly', False)]})
    num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')
    total_amount = fields.Float(string='Total amount', compute='get_total_amount')
    line_ids = fields.One2many(comodel_name='cash.advance.line', inverse_name='advance_id', string="Request Lines", copy=True, readonly=True, states={'draft': [('readonly', False)]})
    paid = fields.Boolean(string="Paid")
    move_id = fields.Many2one(comodel_name="account.move", string="Accounting Entry", readonly=True)
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal")

    def _get_company(self):
        return self.env.user.company_id

    company_id = fields.Many2one(comodel_name="res.company", string="Company", default=_get_company, required=True, readonly=True, states={'draft': [('readonly', False)]})

    def _get_employee_manager(self):
        self.manager_id = self.employee_id.parent_id and self.employee_id.parent_id.id or self.department_id.manager_id and self.department_id.manager_id.id or False
    
    def submit(self):
        if not self.line_ids:
            raise UserError("No advance lines found!")
        self.write({'state': 'submit'})
        partner_ids = []
        if self.employee_id.parent_id.user_id:
            partner_ids.append(self.employee_id.parent_id.user_id.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Cash advance Request '{}', for {} needs approval".format(self.name, self.employee_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
        return True

    def mgr_approve(self):
        self.name = self.env['ir.sequence'].next_by_code('cash.advance')
        group_id = self.env['ir.model.data'].xmlid_to_object('account.group_account_user')
        partner_ids = []
        user_ids = []
        for user in group_id.users:
            user_ids.append(user.id)
            partner_ids.append(user.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Cash advance Request '{}', for {} has been approved by Manager".format(self.name, self.employee_id.name)
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
        self.state = "mgr_approve"

    def unlink(self):
        for advance in self:
            if self.filtered(lambda advance: advance.state not in ('draft')):
                raise UserError("You can't delete an advance that is not in draft state")
        return super(CashAdvance, self).unlink()
        
    def finance_approve(self):
        self.state = "approve"
        partner_ids = [self.user_id.partner_id.id]
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Cash advance Request '{}', has been approved by Finance".format(self.name)
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def get_total_amount(self):
        for advance in self:
            total_amount = 0.0
            for line in advance.line_ids:
                total_amount += line.amount
            advance.total_amount = total_amount
    
    def button_reject(self):
        self.write({'state':'reject'})
        subject = "Cash advance Request '{}', for {} has been rejected".format(self.name, self.employee_id.name)
        partner_ids = [self.user_id.partner_id.id]       
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
    
    def set_to_draft(self):
        self.write({'state':'draft'})
        
    def post_entries(self):
        if self.move_id:
            return
        requesting_partner = self.employee_id.user_id.partner_id
        move_vals = {
            'ref': self.name,
            'date': date.today(),
            'journal_id': self.journal_id.id,
            'line_ids': [(0,0, {
                'name': self.name,
                'debit': self.total_amount > 0 and self.total_amount,
                'credit': 0.0,
                'account_id': requesting_partner.property_account_receivable_id.id, #Debit employee receivable
                'date_maturity': date.today(),
                'partner_id': requesting_partner.id,
                }),
                (0,0, {
                'name': self.name,
                'credit': self.total_amount > 0 and self.total_amount,
                'debit': 0.0,
                'account_id': self.journal_id.default_credit_account_id.id,
                'date_maturity': date.today(),
                'partner_id': requesting_partner.id,
                })
            ]
        }
        account_move = self.env['account.move'].sudo().create(move_vals)
        self.move_id = account_move.id
        self.paid = True
        return True

    
class CashAdvanceLine(models.Model):
    _name = 'cash.advance.line'
    _description = 'advance Lines'
    
    advance_id = fields.Many2one(comodel_name='cash.advance', string='advance')
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    name = fields.Char(string='Description', required=True)
    account_id = fields.Many2one(comodel_name="account.account", string='Account')
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string='Analytic Account')
    quantity = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Float(string="Unit Price")
    amount = fields.Float(string='Amount', required=True, compute="compute_amount")
    state = fields.Selection(string="State", related="advance_id.state")

    def compute_amount(self):
        for line in self:
            line.amount = line.price_unit * line.quantity

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            return {
                'value': {
                    'name': self.product_id.name,
                    'account_id': self.product_id.property_account_expense_id.id,
                    'price_unit': self.product_id.lst_price,
                }
            }