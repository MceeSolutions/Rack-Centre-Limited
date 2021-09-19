# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Internal Change Module",

    'summary': """
        Internal Change Module""",

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'rc_base', 'rc_service', 'website', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/internal_change_views.xml',
    ],
}
