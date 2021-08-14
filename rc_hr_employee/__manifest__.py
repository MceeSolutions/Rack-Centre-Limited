# -*- coding: utf-8 -*-
{
    'name': "Employee Extension",

    'summary': """
        Employee Extension """,

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'rc_business_dev'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/templates.xml',
        'views/views.xml',
    ],
}
