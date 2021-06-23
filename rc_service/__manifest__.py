# -*- coding: utf-8 -*-
{
    'name': "Command Centre and Service Delivery",

    'summary': """
        Module to Handle Rack Centre's command centre and service delivery requests
        """,

    'description': """

        """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'rc_base', 'documents'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'data/files_data.xml',
        'data/sequence.xml',
        'views/main_menuitems.xml',
        'views/templates.xml',
    ],
}
