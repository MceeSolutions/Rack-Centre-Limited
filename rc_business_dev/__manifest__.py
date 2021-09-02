# -*- coding: utf-8 -*-
{
    'name': "Business Development Module",

    'summary': """
        Business Development Module""",

    'description': """
        Business Development Module
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Uncategorized',
    'version': '0.1.1',

    'depends': ['base', 'sale_management', 'sale', 'rc_base'],

    'data': [
        'security/user_groups.xml',
        'data/sequence.xml',
        'views/sale_view.xml',
        'views/res_config_settings_view.xml',
    ],
}
