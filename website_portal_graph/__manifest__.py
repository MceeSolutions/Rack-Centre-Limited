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

{
    'name': 'Website Portal Graph',
    "version" : "14.0.1.0",
    'category': 'Website',
    'summary': 'Website Portal Graph',
    'website': 'https://www.geminatecs.com',
    'author' : 'Geminate Consultancy Services',
    "license": "Other proprietary",
    'depends': ['website','sale_management','account'],
    "description": """
         Geminate comes with feature to analysis your sales quotations, sale order and sales invoice based on various filter like  month wise or year wise. even you can apply group on customer to review the result in animated graphs.
    """,
    'data': [
            'views/portal_templates.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
    "price": 49.99,
    "currency": 'EUR',
}
