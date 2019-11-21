from odoo import models, fields
import requests
import json
from ..helper.rut_helper import calculate_dv


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

        if res.status_code == 200:

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

                        dv = calculate_dv(dte['RUTEmisor'])
                        rut = '{}-{}'.format(dte['RUTEmisor'], dv)

                        detail_res = requests.request(
                            'GET',
                            'https://dev-api.haulmer.com/v2/dte/document/{}/{}/{}/json'.format(
                                rut,
                                dte['TipoDTE'],
                                dte['Folio']
                            ),
                            headers={
                                'apikey': self.api_key
                            }
                        )
                        detail_response = json.loads(detail_res.text)

                        if detail_res.status_code == 200:

                            if detail_response['json']:

                                invoice = self.env['account.invoice'].with_context(
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
                                })
                                raise models.ValidationError(type(detail_response))
                                for line in detail_response['json']['Detalle']:
                                    product = self.env['product.product'].search([('name', '=', line['NmbItem'])])

                                    if len(product) == 1 and product.product_tmpl_id.property_account_expense_id.id:
                                        self.env['account.invoice.line'].create({
                                            'secuence': line['NroLinDet'],
                                            'quantity': line['QtyItem'],
                                            'price_unit': line['PrcItem'],
                                            'price_subtotal': line['MontoItem'],
                                            'product_id': product.id,
                                            'invoice_id': invoice.id,
                                            'name': '{} {}'.format(product.name, product.description_purchase),
                                            'account_id': product.product_tmpl_id.property_account_expense_id.id
                                        })
