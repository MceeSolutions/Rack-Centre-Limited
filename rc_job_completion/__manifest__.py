# -*- coding: utf-8 -*-
{
    'name': "Job Completion",

    'summary': """
        Job Completion""",

    'description': """
        Job Completion
    """,

    'author': "MCEE Business Solutions",
    'website': "http://www.mceesolutions.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/job_view.xml',
        # 'views/templates.xml',
    ],
}
