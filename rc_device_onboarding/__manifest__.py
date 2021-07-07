# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Device Onboarding Module",

    'summary': """
        Device Onboarding Module""",

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
        'security/device_onboarding_security.xml',
        'data/sequence.xml',
        'views/device_onboarding_views.xml',
        'views/device_onboarding_portal_views.xml',
    ],
}
