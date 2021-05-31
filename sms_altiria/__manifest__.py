# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


{
    'name': 'Altiria SMS Gateway',
    'version': '13.0.0.0.1',
    'license': 'AGPL-3',
    'category': 'Comunication',
    'sequence': 1,
    'complexity': 'easy',
    'author': 'PESOL, Odoo Community Association (OCA)',
    'depends': [
        'base',
        'mail',
        'sms'
    ],
    'data': [
        'data/sms_status_multicompany.xml',
        'views/company_view.xml',
        'views/partner_view.xml',
        'views/sms_status_view.xml',
        'wizard/sms_composer_views.xml',
        'security/sms_security.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
}
