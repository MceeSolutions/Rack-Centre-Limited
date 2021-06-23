# -*- coding: utf-8 -*-
{
    'name': "Daily Walkaround",

    'summary': """
        Daily Walkaround Process""",

    'description': """
        Daily Walkaround Process
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'rc_data_centre'],

    # always loaded
    'data': [
        'security/access_groups.xml',
        'security/ir.model.access.csv',
        'views/daily_walkaround_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
