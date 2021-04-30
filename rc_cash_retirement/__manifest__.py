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

    'depends': ['account', 'rc_cash_advance', 'rc_base'],

    'data': [
        'security/user_groups.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/retirement_view.xml',
    ],
}