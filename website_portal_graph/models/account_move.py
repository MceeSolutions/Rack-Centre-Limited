# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api, _
from datetime import datetime
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    # @api.multi
    def get_customer_invoice_values(self,user_id,filter):
        partner = self.env.user.partner_id
        if filter=='customer':
            invoices = self.env['account.move'].search([('state', 'in', ['posted'])])
        elif filter=='open':
            invoices = self.env['account.move'].search([('state', 'in', ['posted']),('payment_state', 'in', ['not_paid'])])
        elif filter=='paid':
            invoices = self.env['account.move'].search([('payment_state', 'in', ['paid'])])

        myLabels  =[]
        myData_dict = {}
        myData =[]
        res ={}
        if invoices:
            for invoice in invoices:
                myData_dict.update({invoice.partner_id.name : invoice.amount_total})
            for data in myData_dict:
                myData.append(myData_dict[data])
                myLabels.append(data)
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        else:
            return False

    # @api.multi
    def get_invocie_date_values(self,user_id,filter):
        partner = self.env.user.partner_id
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        if filter == 'default':
            invoices = self.env['account.move'].search([('state', 'in', ['posted']),('payment_state', 'in', ['paid'])],order='date asc')
        elif filter == 'open':
            invoices = self.env['account.move'].search([('state', 'in', ['posted']),('payment_state', 'in', ['not_paid'])],order='date asc')
        elif filter == 'paid':
            invoices = self.env['account.move'].search([('payment_state', '=', 'paid')])
        
        myLabels  =[]
        myData = []
        res ={}
        date_dict = {}
        if invoices:
            for invoice in invoices:
                is_copy = False
                date_value = (invoice.date)
                date_child_dict = {'month':date_value.month,'year':date_value.year,'total': invoice.amount_total}
                for items in date_dict:
                    if date_dict[items]['month'] == date_value.month and date_dict[items]['year'] == date_value.year:
                        is_copy = True
                        date_dict[items].update({'month':date_value.month,'year':date_value.year,'total': invoice.amount_total + date_dict[items]['total']})
                if not is_copy:
                    date_dict.update({str(date_child_dict['month']) + '-' + str(date_child_dict['year']):date_child_dict})

            for vals in date_dict:
                myLabels.append(str(month_list[date_dict[vals]['month'] - 1]) + str(date_dict[vals]['year']))
                myData.append(str(date_dict[vals]['total']))
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        else :
            return False
        
    # @api.multi
    def get_invoice_values_by_year_month(self,user_id,start_date,end_date,filter,type):
        partner = self.env.user.partner_id
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        if type == 'open':
            invoices = self.env['account.move'].search([('state', 'in', ['posted']),('payment_state', 'in', ['not_paid']),('invoice_date','>=',start_date),('invoice_date','<=',end_date)],order='date asc')
        elif type == 'paid':
            invoices = self.env['account.move'].search([('payment_state', 'in', ['paid']),('invoice_date','>=',start_date),('invoice_date','<=',end_date)],order='date asc')
        else :
            invoices = self.env['account.move'].search([(('state', 'in', ['posted']),('payment_state', 'in', ['paid'])),('invoice_date','>=',start_date),('invoice_date','<=',end_date)],order='date asc')
        myLabels  =[]
        myData = []
        res ={}
        date_dict = {}
        if invoices:
            if filter == 'month':
                for invoice in invoices:
                    is_copy = False
                    date_value = (invoice.date)
                    date_child_dict = {'month':date_value.month,'year':date_value.year,'total': invoice.amount_total}
                    for items in date_dict:
                        if date_dict[items]['month'] == date_value.month and date_dict[items]['year'] == date_value.year:
                            is_copy = True
                            date_dict[items].update({'month':date_value.month,'year':date_value.year,'total': invoice.amount_total + date_dict[items]['total']})
                    if not is_copy:
                        date_dict.update({str(date_child_dict['month']) + '-' + str(date_child_dict['year']):date_child_dict})
                
                for vals in date_dict:
                    myLabels.append(str(month_list[date_dict[vals]['month'] - 1]) + str(date_dict[vals]['year']))
                    myData.append(str(date_dict[vals]['total']))
                res.update({
                            'my_data':myData,
                            'my_labels':myLabels
                            })
                return res
            elif filter == 'year':
                for invoice in invoices:
                    is_copy = False
                    date_value = (invoice.invoice_date)
                    date_child_dict = {'year':date_value.year,'total': invoice.amount_total}
                    for items in date_dict:
                        if date_dict[items]['year'] == date_value.year:
                            is_copy = True
                            date_dict[items].update({'year':date_value.year,'total': invoice.amount_total + date_dict[items]['total']})
                    if not is_copy:
                        date_dict.update({str(date_child_dict['year']):date_child_dict})
                for vals in date_dict:
                    myLabels.append(date_dict[vals]['year'])
                    myData.append(date_dict[vals]['total'])
                res.update({
                            'my_data':myData,
                            'my_labels':myLabels
                            })
                return res
        else :
            return False
        
    # @api.multi
    def get_customer_due_invoice_values(self, user_id):
        partner = self.env.user.partner_id
        invoices = self.env['account.move'].search([('state', 'in', ['posted']),('payment_state', 'in', ['not_paid'])], order='invoice_date_due asc')
        myLabels=[]
        myData=[]
        res={}
        myData_dict={}
        if invoices:
            for invoice in invoices:
                myData_dict.update({invoice.partner_id.name + ' ('  + str(invoice.invoice_date_due) + ')': invoice.amount_total})
            for data in myData_dict:
                myData.append(myData_dict[data])
                myLabels.append(data)
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        else :
            return False
