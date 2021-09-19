# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Cross Connect Module",

    'summary': """
        Cross Connect Module""",

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
        'security/cross_connect_security.xml',
        'views/cross_connect_views.xml',
        'views/cross_connect_portal_views.xml',
        'views/res_partner_views.xml',
    ],
}
