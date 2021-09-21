# -*- coding: utf-8 -*-
{
    'name': "Account Move Dump",

    'summary': """
        Account Move Dump""",

    'description': """
        Account move dump
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Account',
    'version': '0.1',

    'depends': ['account'],

    'data': [
        'security/ir.model.access.csv',
        'views/account_view.xml',
    ],
}
