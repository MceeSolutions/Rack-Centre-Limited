from datetime import date
from odoo import models, fields


class VendorQualification(models.Model):
    _name = 'vendor.qualification'
    _description = 'Vendor Qualification'

    name = fields.Char(string="Potential Vendor Name")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    reg_number = fields.Char(string="Registration Number")
    phone = fields.Char(string="Phone")
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    contact_name = fields.Char(string="Contact Person")
    contact_phone = fields.Char(string="Contact Phone")
    contact_email = fields.Char(string="Contact Email")
    category = fields.Char(string="Category")
    state = fields.Selection(selection=[
        ('draft', 'New'),
        ('submit', 'Validate'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
    ], default="draft", help="""
    When a request is created, state is draft, 
    when the creator confirms that all is fine, it moves to submit
    After reviewing the document provided by the vendor, the project manager approves it
    """)
    partner_id = fields.Many2one(comodel_name='res.partner', string="Vendor")
    date_submitted = fields.Date(string="Submitted on", readonly=True)
    submitted_by = fields.Many2one(comodel_name="res.users", string="Submitted by", readonly=True)
    approved_by = fields.Many2one(comodel_name="res.users", string="Approved By", readonly=True)
    date_approved = fields.Date(string="Approved on", readonly=True)
    vendor_count = fields.Integer(string="Vendors", compute="get_vendors")

    def get_vendors(self):
        self.vendor_count = len(self.partner_id)

    def action_view_vendor(self):
        action = self.env.ref('account.action_move_out_invoice_type')
        result = action.read()[0]
        result['context'] = {'type': 'out_invoice'}
        related_invoices = self.env['account.move'].search([('treatment_id', '=', self.id)])
        if self.invoice_count != 1:
            result['domain'] = "[('id', 'in', " + str(related_invoices.ids) + "), ('move_type', '=', 'out_invoice')]"
        elif self.invoice_count == 1:
            res = self.env.ref('account.view_move_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = related_invoices.id
        return result
        pass 

    def submit(self):
        self.submitted_by = self.env.uid
        self.date_submitted = date.today()        
        self.state = 'submit'

    def approve(self):
        vendor = self.env['res.partner'].create({
            'name': self.name,
            'supplier_rank': 1,
            'email': self.email,
            'phone': self.phone,
            'website': self.website,
            'street': self.street,
            'city': self.city,
            'child_ids': [(0, 0, {
                'name': self.contact_name,
                'phone': self.contact_phone,
                'email': self.contact_email,
            })],
        })
        self.approved_by = self.env.uid
        self.date_approved = date.today()
        self.partner_id = vendor.id
        self.state = 'approve'

    def reject(self):
        self.state = 'reject'

    def re_open(self):
        self.state = 'draft'