# Copyright 2017 Pesol (<http://pesol.es>)
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import models, api, fields, _
from odoo.exceptions import UserError
from odoo import exceptions
import requests


class SmsStatus(models.Model):
    _name = 'sms.status'
    _order = 'create_date desc'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner')

    phone_number = fields.Char(
        string='Phone Number')

    model_name = fields.Char(
        string='Model name')

    model_id = fields.Integer(
        string='Model Id')

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        default=lambda self: self.env.user.id)

    sended = fields.Boolean(
        string='Sended')

    company_id = fields.Many2one(
        comodel_name='res.company',
        related='user_id.company_id',
        store=True,
        string='Company')

    status = fields.Char(
        string='Status')
    
    def get_credit(self):
        url = 'http://www.altiria.net/api/http'
        company = self.env.user.company_id
        payload = {
            'cmd': 'getcredit',
            'login': company.sms_login,
            'passwd': company.sms_passwd
        }
        if company.sms_domain:
            payload.update({
                'domainId': company.sms_domain
            })
        contentType = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        r = requests.post(url, data=payload,
                          headers=contentType, timeout=(5, 60))
        valid = str(r.content).find('OK')
        if valid == -1:
            raise UserError(r.text)
        raise UserError(
            _('Saldo Disponible: ' + r.text.split(':')[1]))
