# -*- coding: utf-8 -*-
{
    'name': "Contact Extension Module",

    'summary': """
        Extension of the Contact module""",

    'description': """
        Extension of the Contact module
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'CRM',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/res_partner.xml',
        # 'views/templates.xml',
    ],
}
