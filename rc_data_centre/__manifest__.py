# -*- coding: utf-8 -*-
{
    'name': "Data Centre and Facility",

    'summary': """
        Data Centre and Facility""",

    'description': """
        Data Centre and Facility
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/data_centre_view.xml',
        'views/tool_management_view.xml',
        'views/material_gate_pass_view.xml',
    ],
}
