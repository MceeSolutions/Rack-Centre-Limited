# -*- coding: utf-8 -*-
{
    'name': "Part Replacement",

    'summary': """
        Part Replacement""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'account_asset', 'product'],

    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/part_replacement_view.xml',
    ],
}
