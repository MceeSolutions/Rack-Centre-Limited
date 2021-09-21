# -*- coding: utf-8 -*-
{
    'name': "Dashboard Enhancement Module",

    'summary': """
        Dashboard Enhancement Module""",

    'description': """
        Dashboard Enhancement Module
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Uncategorized',
    'version': '0.1.1',

    'depends': [
        'base',
        'website',
        # 'ks_dashboard_ninja',
        # 'ks_dn_advance',
    ],

    # always loaded
    'data': [
        # Load the snippets (building block code) when installing
        'views/snippets.xml',
    ]
}
