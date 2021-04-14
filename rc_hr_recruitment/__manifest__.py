# -*- coding: utf-8 -*-
{
    'name': "Recruitment Enhancement Module",

    'summary': """
        Extension to track your recruitment pipeline """,

    'description': """
        
    """,

    'author': "Mcee Business Solution",
    'website': "https://www.mceesolutions.com",
    'category': 'Human Resources/Recruitment',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_recruitment'],

    # always loaded
    'data': [
        # 'views/templates.xml',
        #'views/views.xml',
        'views/rc_recruitment_request.xml',
        'security/rc_hr_recruitment_security.xml',
        'security/ir.model.access.csv',
    ],

}
