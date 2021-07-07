# -*- coding: utf-8 -*-
{
    'name': "Rack Centre Equipment Relocation Module",

    'summary': """
        Equipment Relocation Module""",

    'description': """
        
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'rc_base', 'rc_service', 'documents'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/equipment_relocation_security.xml',
        'data/sequence.xml',
        'views/equipment_relocation_views.xml',
        'views/equipment_relocation_portal_views.xml',
    ],
}
