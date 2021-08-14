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
    'depends': ['base', 'rc_base', 'rc_service', 'website', 'hr'],

    # always loaded
    'data': [
        'security/access_request_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/cron.xml',
        'data/access_category_data.xml',
        'views/access_request_views.xml',
        'views/access_category_views.xml',
        'views/access_request_lines.xml',
        'views/access_request_website_template.xml',
    ],
}