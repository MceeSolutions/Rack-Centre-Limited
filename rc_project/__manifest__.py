# -*- coding: utf-8 -*-
{
    'name': "rc_project",

    'summary': """
        Extension of the project module""",

    'description': """
        Extension of the project module
    """,

    'author': "Mcee Business Solutions",
    'website': "https://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Services/Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'rc_base', 'project', 'purchase_requisition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'data/sequence.xml',
        'wizard/project_resource_wizard_views.xml',
        'views/views.xml',
        'views/business_case_views.xml',
        'views/lessons_learned_views.xml',
        'views/change_management_views.xml',
        'views/risk_identification_views.xml',
        'views/issue_form_views.xml',
        'views/rca_form_views.xml',
        'views/project_schedule_views.xml',
        # 'views/templates.xml',
    ],
}
