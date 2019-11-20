from odoo import models, fields
import requests
import json
from datetime import datetime


class ResCompany(models.Model):
    _inherit = 'res.company'

    api_key = fields.Char('Api Key')

    idempotency_key = fields.Char('Idempotency Key')

    def sync_received_invoice(self):
        res = requests.request(
            'POST',
            'https://dev-api.haulmer.com/v2/dte/document/received',
            headers={
                'apikey': self.api_key
            }
        )

        response = json.loads(res.text)

        if response['data']:
            for dte in response['data']:
                tmp = self.env['account.invoice'].search([('dte_folio', '=', dte['Folio'])])
                if len(tmp) == 0:
                    provider = self.env['res.partner'].search([('name', '=', dte['RznSoc'])])
                    partner_id = None
                    if len(provider) == 1:
                        partner_id = provider.id
                    self.env['account.invoice'].create({
                        'dte_folio': dte['Folio'],
                        'dte_type_id': dte['TipoDTE'],
                        'dte_payment_mode_id': dte['FmaPago'],
                        'date_invoice': datetime.strptime(dte['FchEmis'], '%Y-%m-%d'),
                        'amount_untaxed': dte['MntNeto'],
                        'amount_tax': dte['IVA'],
                        'amount_total': dte['MntTotal'],
                        'partner_id': partner_id
                    })
                    raise models.ValidationError(res.text)
