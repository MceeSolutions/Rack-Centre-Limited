# -*- coding: utf-8 -*-
{
    'name': "Extension of Website CRM Contact Form",

    'summary': """
        Extension of Website CRM Contact Form """,

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "http://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Website/Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_crm', 'crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'data/website_crm_data.xml',
        'views/website_crm_template.xml',
    ],
}
