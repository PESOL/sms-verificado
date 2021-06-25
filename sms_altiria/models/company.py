# Copyright 2017 Pesol (<http://pesol.es>)
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class Company(models.Model):
    _inherit = 'res.company'

    sms_login = fields.Char(
        string='SMS Login')

    sms_passwd = fields.Char(
        string='SMS Password')

    sms_sender = fields.Char(
        string='SenderId')
