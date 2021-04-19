# -*- coding: utf-8 -*-
{
    'name': "Procurement Enhancement Module",

    'summary': """
        Procurement Enhancement Module""",

    'description': """
        Procurement Enhancement Module
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Uncategorized',
    'version': '0.1.1',

    'depends': [
        'purchase', 
        'purchase_requisition',
        'project',
    ],

    'data': [
        # 'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/vendor_qualification_view.xml',
    ],
}
