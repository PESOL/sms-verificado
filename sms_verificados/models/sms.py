# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import requests

from openerp import models, api, _


class SmsApi(models.AbstractModel):
    _inherit = 'sms.api'

    @api.model
    def _send_sms(self, numbers, message):
        active_model = self.env.context.get('default_res_model') or\
            self.env.context.get('active_model')
        model = self.env[active_model]
        company = self.env.user.company_id
        create_log = False
        if self.env.context.get('default_composition_mode') == 'mass':
            create_log = True
        sms_status_obj = self.env['sms.status']
        url = 'http://web.smsverificados.net/api/http'
        user_id = self.env.user and self.env.user.id
        try:
            payload = {
                'cmd': 'sendsms',
                'login': company.sms_login,
                'passwd': company.sms_passwd,
                'senderId': company.sms_sender,
                'source': 'odoo',
                'msg': message,
                'concat': 'true'
            }
            for number in numbers:
                number_search = number
                number = number.replace('+', '')
                number = number.replace(' ', '')
                if len(number) == 9:
                    if number.startswith('6') or number.startswith('7'):
                        payload.update({'dest': '34' + number})
                        number = '34' + number
                    else:
                        payload.update({'dest': number})
                elif len(number) == 11:
                    payload.update({'dest': number})
                try:
                    if active_model == 'res.partner':
                        partner_id = False
                        if self.env.context.get('default_res_id'):
                            res_id = int(self.env.context.get(
                                'default_res_id'))
                            partner_id = model.browse(res_id)
                        if not partner_id:
                            partner_id = model.search([
                                ('mobile', 'like', number)
                            ])
                            if not partner_id:
                                partner_id = model.search([
                                    ('mobile', 'like', number[2:].strip())
                                ])
                            if not partner_id:
                                partner_id = model.search([
                                    ('mobile', 'like', number_search)
                                ])
                        if not partner_id:
                            continue
                        sms_status_id = sms_status_obj.create({
                            'partner_id': partner_id.id,
                            'model_name': _(partner_id._description),
                            'model_id': partner_id.id,
                            'phone_number': number,
                            'user_id': user_id
                        })
                        if create_log:
                            subtype_id = self.env['mail.message.subtype'].search([
                                ('name', '=', 'Note')
                            ])
                            self.env['mail.message'].create({
                                'message_type': 'sms',
                                'subtype_id': subtype_id.id,
                                'res_id': partner_id.id,
                                'model': partner_id._name,
                                'author_id': self.env.user.partner_id.id,
                                'email_from': self.env.user.partner_id.email,
                                'body': message
                            })
                    else:
                        active_id = self.env.context.get('default_res_ids') or\
                            self.env.context.get('default_res_id')
                        model_ids = self.env[model._name].browse(active_id)
                        model_id = model_ids.filtered(
                            lambda l: l.partner_id and
                            l.partner_id.mobile.strip().replace(
                                '+', '').replace(' ', '') == number[2:]
                            or l.partner_id.mobile and
                            l.partner_id.mobile.strip().replace(
                                '+', '').replace(' ', '') == number
                            or l.mobile and l.mobile == number[2:]
                            or l.mobile and l.mobile == number)
                        if not model_id:
                            continue
                        sms_status_id = sms_status_obj.create({
                            'partner_id': model_id.partner_id.id,
                            'model_name': _(model_id._description),
                            'model_id': model_id.id,
                            'phone_number': number,
                            'user_id': user_id
                        })
                        if create_log:
                            subtype_id = self.env['mail.message.subtype'].search([
                                ('name', '=', 'Note')
                            ])
                            self.env['mail.message'].create({
                                'message_type': 'sms',
                                'subtype_id': subtype_id.id,
                                'res_id': model_id.id,
                                'model': model_id._name,
                                'author_id': self.env.user.partner_id.id,
                                'email_from': self.env.user.partner_id.email,
                                'body': message
                            })
                except Exception as e:
                    raise e
                contentType = {
                    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
                r = requests.post(url, data=payload,
                                  headers=contentType, timeout=(5, 60))
                valid = str(r.content).find('OK')
                if valid != -1:
                    sms_status_id.write({
                        'sended': True,
                        'status': str(r.content)[2:4]
                    })
                else:
                    sms_status_id.write({
                        'sended': False,
                        'status': str(r.text)
                    })
        except requests.ConnectTimeout:
            print("Tiempo de conexión agotado")
        except requests.ReadTimeout:
            print("Tiempo de respuesta agotado")
        except Exception as ex:
            print("Error interno: " + str(ex))

    @api.model
    def _send_sms_batch(self, messages):
        numbers = []
        msg = messages[0].get('content')
        for message in messages:
            numbers.append(message.get('number'))
        self._send_sms(numbers, msg)
