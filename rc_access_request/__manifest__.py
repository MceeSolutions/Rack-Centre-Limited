# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Access Request Module",

    'summary': """
        Access Request Module""",

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
        'security/access_request_security.xml',
        'data/sequence.xml',
        'data/cron.xml',
        'views/access_request_views.xml',
        'views/access_request_website_template.xml',
    ],
}