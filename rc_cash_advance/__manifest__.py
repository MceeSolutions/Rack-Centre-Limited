# -*- coding: utf-8 -*-
{
    'name': "Cash Advance",

    'summary': """
        Employee Cash Advance""",

    'description': """
        Employee Cash Advance
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Account',
    'version': '0.1',

    'depends': ['account', 'rc_base'],

    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'data/sequence.xml',
        'views/advance_view.xml',
    ],
}