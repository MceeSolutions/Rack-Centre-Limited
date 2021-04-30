# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError


class CashRetirement(models.Model):
    _name = 'cash.retirement'
    _description = 'Cash retirement Request Form'
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
    
    name = fields.Char(string='Order Reference', readonly=True, required=True, index=True, copy=False, default='/')
    note = fields.Char(string="Description", readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'New'),
        ('submit', 'Submitted'),
        ('mgr_approve', 'Line Manager Approved'),
        ('approve', 'Finance Approved'),
        ('close', 'Retired'),
        ('reject', 'Reject'),
        ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking='1')

    date = fields.Date(string='Date', required=True, tracking='1', default=date.today(), readonly=True, states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one(comodel_name='hr.employee', required=True, string='Employee', tracking='1', default=_default_employee, readonly=True, states={'draft': [('readonly', False)]})
    manager_id = fields.Many2one(comodel_name="hr.employee", string="Employee Manager", compute="_get_employee_manager")
    department_id = fields.Many2one(comodel_name='hr.department', string='Department', related='employee_id.department_id')
    currency_id = fields.Many2one(comodel_name='res.currency', required=True, string='Currency', default=_default_currency, readonly=True, states={'draft': [('readonly', False)]})
    num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')
    total_amount = fields.Float(string='Total amount', compute='get_total_amount', readonly=True)
    line_ids = fields.One2many(comodel_name='cash.retirement.line', inverse_name='retirement_id', string="Request Lines", copy=True, readonly=True, states={'draft': [('readonly', False)]})
    move_ids = fields.Many2many(comodel_name="account.move", string="Accounting Entry", readonly=True)
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal")
    advance_id = fields.Many2one(comodel_name="cash.advance", string="Cash Advance", readonly=True, 
    states={'draft': [('readonly', False)]}, domain="[('user_id', '=', user_id), ('state', 'in', ['approve'])]")
    amount_advance = fields.Monetary(string="Advance Amount", related="advance_id.move_id.amount_total")
    invoices_count = fields.Integer(string="Invoices", compute="count_invoices")
    user_id = fields.Many2one(comodel_name='res.users', required=True, string='User', default=_get_user, readonly= True, states={'draft': [('readonly', False)]})
    payment_account_id = fields.Many2one('account.account', string="Account")

    def _get_company(self):
        return self.env.user.company_id

    company_id = fields.Many2one(comodel_name="res.company", string="Company", default=_get_company, required=True, readonly=True, states={'draft': [('readonly', False)]})

    def _get_employee_manager(self):
        self.manager_id = self.employee_id.parent_id and self.employee_id.parent_id.id or self.department_id.manager_id and self.department_id.manager_id.id or False

    def count_invoices(self):
        self.invoices_count = len(self.move_ids.ids)

    def action_view_invoices(self):
        action = self.env.ref('account.action_move_journal_line')
        result = action.read()[0]
        if len(self.move_ids) != 1:
            result['domain'] = "[('id', 'in', " + str(self.move_ids.ids) + ")]"
        elif len(self.move_ids) == 1:
            res = self.env.ref('account.view_move_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.move_ids.id
        return result

    
    def unlink(self):
        if any(self.filtered(lambda advance: advance.state not in ['draft'])):
            raise UserError("You can't delete a retirement that is not in draft state")
        res = super(CashRetirement, self).unlink()
        return res 
    
    @api.onchange('advance_id')
    def onchange_advance_id(self):
        if self.advance_id:
            self.line_ids.unlink()
            line_copy = [(0, 0, {
                'product_id': line.product_id.id, 
                'name': line.name, 
                'account_id': line.account_id.id,
                'analytic_account_id': line.analytic_account_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'amount': line.amount,
                }
            ) 
            for line in self.advance_id.line_ids]
            return {
                'value': {
                    'line_ids': line_copy
                }
            } 
    
    
    def submit(self):
        if not self.line_ids:
            return UserError("Please add lines!")
        self.write({'state': 'submit'})
        partner_ids = [self.manager_id.user_id.partner_id.id]
        if self.employee_id.parent_id.user_id:
            partner_ids.append(self.employee_id.parent_id.user_id.partner_id.id)
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Cash retirement Request '{}', for {} needs approval".format(self.name, self.employee_id.name)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)
        return False

    def mgr_approve(self):
        self.name = self.env['ir.sequence'].next_by_code('cash.retirement')
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

    def finance_approve(self):
        self.state = "approve"
        partner_ids = [self.user_id.partner_id.id]
        self.message_subscribe(partner_ids=partner_ids)
        subject = "Cash advance Request '{}', has been approved by Finance".format(self.name)
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    
    def button_reject(self):
        self.write({'state':'reject'})
        subject = "Cash advance Request '{}', for {} has been rejected".format(self.name, self.employee_id.name)
        partner_ids = [self.user_id.partner_id.id]       
        for partner in self.message_partner_ids:
            partner_ids.append(partner.id)
        self.message_post(subject=subject,body=subject,partner_ids=partner_ids)

    
    def set_to_draft(self):
        self.write({'state':'draft'})
    
    def get_total_amount(self):
        for retirement in self:
            total_amount = 0.0
            for line in retirement.line_ids:
                total_amount += line.amount
            retirement.total_amount = total_amount

    def post_entries(self):
        if not self.journal_id:
            raise UserError("Please specify a journal")
        requesting_partner = self.employee_id.user_id.partner_id
        account_moves = self.env['account.move']
        move_vals = {
            'ref': self.name,
            'date': date.today(),
            'journal_id': self.journal_id.id,
            'amount_total': self.total_amount,
            'line_ids': [(0,0, { # Debit the expense account
                'name': self.name,
                'debit': line.amount,
                'credit': 0.0,
                'account_id': line.account_id.id, # Debit employee receivable
                'date_maturity': date.today(),
                'partner_id': self.employee_id.user_id.partner_id.id,
                }) for line in self.line_ids] + [
                    (0,0, {
                        'name': self.name,
                        'credit': self.total_amount,
                        'debit': 0.0,
                        'account_id': self.employee_id.user_id.partner_id.property_account_receivable_id.id,
                        'date_maturity': date.today(),
                        'partner_id': self.employee_id.user_id.partner_id.id,
                    })
            ]
        }
        account_move = self.env['account.move'].sudo().create(move_vals)
        account_moves += account_move
        if self.amount_advance != self.total_amount:
            if self.total_amount > self.amount_advance: 
                account_move = self.env['account.move'].create({
                    'ref': self.name,
                    'date': date.today(),
                    'journal_id': self.journal_id.id,
                    'amount_total': abs(self.total_amount - self.amount_advance),
                    'line_ids': [(0,0, { # Debit
                        'name': self.name,
                        'debit': abs(self.total_amount - self.amount_advance),
                        'credit': 0.0,
                        'account_id': self.employee_id.user_id.partner_id.property_account_receivable_id.id,
                        'date_maturity': date.today(),
                        'partner_id': self.employee_id.user_id.partner_id.id,
                        }),
                            (0,0, {
                                'name': self.name,
                                'credit': abs(self.total_amount - self.amount_advance),
                                'debit': 0.0,
                                'account_id': self.payment_account_id.id, # Debit employee receivable
                                'date_maturity': date.today(),
                                'partner_id': self.employee_id.user_id.partner_id.id,
                            })
                    ]
                })
            else:
                account_move = self.env['account.move'].create({
                    'ref': self.name,
                    'date': date.today(),
                    'journal_id': self.journal_id.id,
                    'amount_total': abs(self.total_amount - self.amount_advance),
                    'line_ids': [(0,0, { # Debit
                        'name': self.name,
                        'debit': abs(self.total_amount - self.amount_advance), # Debit employee receivable,
                        'credit': 0.0,
                        'account_id': self.payment_account_id.id, # Debit employee receivable
                        'date_maturity': date.today(),
                        'partner_id': self.employee_id.user_id.partner_id.id,
                        }), (0,0, {
                                'name': self.name,
                                'credit': abs(self.total_amount - self.amount_advance),
                                'debit': 0.0,
                                'account_id': self.employee_id.user_id.partner_id.property_account_receivable_id.id,
                                'date_maturity': date.today(),
                                'partner_id': self.employee_id.user_id.partner_id.id,
                            })
                    ]
                })
            account_moves += account_move
        self.move_ids += account_moves
        self.paid = True
        self.advance_id.state = "close"
        self.state = "close"
        return True


class CashRetirementLine(models.Model):
    _name = 'cash.retirement.line'
    _description = 'retirement Lines'
    
    retirement_id = fields.Many2one(comodel_name='cash.retirement', string='retirement')
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    name = fields.Char(string='Description', required=True)
    account_id = fields.Many2one(comodel_name="account.account", string='Account')
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string='Analytic Account')
    quantity = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Float(string='Unit price')
    amount = fields.Float(string='Amount', required=True, compute="compute_amount")
    state = fields.Selection(string="State", related="retirement_id.state")

    
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
