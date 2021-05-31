# Copyright 2017 Pesol (<http://pesol.es>)
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    sms_out = fields.Boolean(
        string='SMS out',
        help="Mark this field if partner don't want to recieve SMS")
