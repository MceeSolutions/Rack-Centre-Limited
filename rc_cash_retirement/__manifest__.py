# -*- coding: utf-8 -*-
{
    'name': "Cash retirement",

    'summary': """
        Employee Cash retirement""",

    'description': """
        Employee Cash retirement
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Account',
    'version': '0.1',

    'depends': ['account', 'sunray_cash_advance'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/user_groups.xml',
        'views/retirement_view.xml',
    ],
}