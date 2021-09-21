from odoo import models, fields


class AccountMove(models.Model):

    _name = 'account.move.dump'
    _description = 'Journal Entries Historical Data'

    name = fields.Char(string="Main Account Name")
    code = fields.Char(string="Main Account Code")
    document_date = fields.Date(string="Account")
    tnx_code = fields.Char(string="Transaction Code")
    document_number = fields.Char(string="Document Number")
    reference_number = fields.Char(string="Reference Number")
    division = fields.Char(string="Division")
    department = fields.Char(string="Department")
    narration = fields.Char(string="Narration")
    debit = fields.Float(string="Debits")
    credit = fields.Float(string="Credits")
    balance = fields.Float(string="Balance amount")
