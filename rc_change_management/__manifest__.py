# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Change Management Module",

    'summary': """
        Change Management Module""",

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'rc_base', 'rc_service'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/change_management_security.xml',
        'data/sequence.xml',
        'views/change_management_views.xml',
        'views/change_management_portal_views.xml',
    ],
}
