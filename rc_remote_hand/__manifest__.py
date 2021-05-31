# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Remote Hand Module",

    'summary': """
        Remote Hand Module""",

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'rc_base', 'rc_service', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/remote_hand_views.xml',
        'views/remote_hand_portal_views.xml',
    ],
}
