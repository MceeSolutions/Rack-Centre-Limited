# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Material Gatepass Portal Module",

    'summary': """
        Material Gatepass Portal""",

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'rc_base', 'rc_service', 'rc_data_centre', 'website'],

    # always loaded
    'data': [
        'security/portal_material_gatepass.xml',
        'security/ir.model.access.csv',
        'views/material_gatepass_views.xml',
        'views/portal_material_gatepass_views.xml',
    ],
}
