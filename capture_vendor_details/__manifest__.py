# -*- coding: utf-8 -*-
{
    'name': "Capture Vendor details from Email",
    'summary': "Wizard to update vendor email and send a notification email in Odoo v17 Community",
    'description': """
        This module provides a wizard to update the vendor's email and send an email notification.
    """,
    'author': "Shivam Soni",
    'website': "",
    'category': 'Contact/Mail',
    'version': '17.0.1.0.0',
    'depends': ['purchase', 'mail', 'website'],
    'license': 'LGPL-3',
    'data': [
        'data/vendor_form_template_data.xml',
        'data/vendor_email_template_data.xml',
        'security/ir.model.access.csv',
        'wizard/update_vendor_email_wizard_view.xml',
        'views/res_partner_views.xml',
        'views/purchase_view.xml',
    ],
    
    'assets': {
        'web.assets_frontend': [
            'capture_vendor_details/static/src/js/get_m2m_values.js',
        ],
        
    }
}
