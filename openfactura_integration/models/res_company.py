from odoo import models, fields
import requests
import json


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
                    dte_type = self.env['dte.type'].search([('code', '=', dte['TipoDTE'])])
                    dte_payment_mode = self.env['dte.payment.mode'].search([('code', '=', dte['FmaPago'])])
                    partner_id = None
                    if len(provider) == 1:
                        partner_id = provider.id

                    reverse = map(int, reversed(str(dte['RUTEmisor'])))
                    factors = cycle(range(2, 8))
                    s = sum(d * f for d, f in zip(reverse, factors))
                    dv = (-s) % 11
                    rut = '{}-{}'.format(dte['RUTEmisor'], dv)
                    raise models.ValidationError(rut)

                    detail_res = requests.request(
                        'GET',
                        'https://dev-api.haulmer.com/v2/dte/document/{}/{}/{}/json'.format(
                            dte['RUTEmisor'],
                            dte['TipoDTE'],
                            dte['Folio']
                        ),
                        headers={
                            'apikey': self.api_key
                        }
                    )
                    detail_response = json.dumps(detail_res.text)

                    raise models.ValidationError(detail_res.text)

                    if detail_response['json']:

                        invoice_lines = []

                        for line in detail_response['json']['Detalle']:
                            product = self.env['product.product'].search(['name', '=', line['NmbItem']])

                            invoice_line = {
                                'secuence': line['NroLinDet'],
                                'quantity': line['QtyItem'],
                                'price_unit': line['PrcItem'],
                                'price_subtotal': line['MontoItem'],
                                'product_id': product.id
                            }

                            invoice_lines.append(invoice_line)

                        if len(invoice_lines) > 0:

                            self.env['account.invoice'].with_context(
                                default_type='in_invoice',
                                type='in_invoice'
                            ).create({
                                'dte_folio': dte['Folio'],
                                'dte_type_id': dte_type.id,
                                'dte_payment_mode_id': dte_payment_mode.id,
                                'date_invoice': dte['FchEmis'],
                                'amount_untaxed': dte['MntNeto'],
                                'amount_tax': dte['IVA'],
                                'amount_total': dte['MntTotal'],
                                'partner_id': partner_id,
                                'invoice_line_ids': invoice_lines
                            })
