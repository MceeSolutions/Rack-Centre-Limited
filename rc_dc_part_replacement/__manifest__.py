# -*- coding: utf-8 -*-
{
    'name': "DC Part Replacement",

    'summary': """
        DC Part Replacement""",

    'description': """
        DC Part Replacement
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'account_asset', 'product', "rc_data_centre"],

    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/part_replacement_view.xml',
    ],
}
