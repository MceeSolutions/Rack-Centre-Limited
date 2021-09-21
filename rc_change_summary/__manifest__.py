# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Change Summary Module",

    'summary': """
        Change Summary Module""",

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'rc_base', 'rc_service'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/change_summary_views.xml',
    ],
}
