# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Equipment Decommissioning Module",

    'summary': """
        Equipment Decommissioning Module""",

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'rc_base', 'rc_service'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/equipment_decommissioning_security.xml',
        'data/sequence.xml',
        'views/equipment_decommissioning_views.xml',
        'views/equipment_decommissioning_portal_views.xml',
    ],
}
