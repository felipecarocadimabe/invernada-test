from odoo import models, fields, api
import requests
import json


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    dte_type_id = fields.Many2one(
        'dte.type',
        'Tipo de Factura'
    )

    dte_payment_mode_id = fields.Many2one(
        'dte.payment.mode',
        'Forma de Pago'
    )

    dte_base64_data = fields.Text(
        'Documento PDF',
        readonly=True
    )

    dte_folio = fields.Integer(
        'Folio',
        readonly=True
    )

    @api.model
    def get_detail_data(self):
        lines = []
        for line in self.invoice_line_ids:
            lines.append({
                'NroLinDet': line.sequence,
                'NmbItem': line.name,
                'QtyItem': line.quantity,
                'PrcItem': line.price_unit,
                'MontoItem': line.price_subtotal
            })
        return lines

    def action_invoice_open(self):
        taxes = []

        for line in self.invoice_line_ids:
            taxes += line.invoice_line_tax_ids.mapped('amount')

        tax = sum(taxes) / len(self.invoice_line_ids)

        data = {
            'response': [
                'PDF', 'FOLIO'
            ],
            'dte': {
                'Encabezado': {
                    'IdDoc': {
                        'TipoDTE': self.dte_type_id.code,
                        'Folio': 0,
                        'FchEmis': str(self.date_invoice),
                        'TpoTranCompra': "1",
                        'TpoTranVenta': "1",
                        'FmaPago': self.dte_payment_mode_id.code

                    },
                    'Emisor': self.company_id.partner_id.get_emitter_data(),
                    'Receptor': self.partner_id.get_receiver_data(),
                    'Totales': {
                        'MntNeto': self.amount_untaxed,
                        'TasaIVA': tax,
                        'IVA': self.amount_tax,
                        'MntTotal': self.amount_total,
                        'MontoPeriodo': self.amount_total,
                        'VlrPagar': self.amount_total
                    }
                },
                'Detalle': self.get_detail_data()
            }
        }

        res = requests.request(
            'POST',
            'https://dev-api.haulmer.com/v2/dte/document',
            headers={
                'apikey': self.company_id.api_key
            },
            data=json.dumps(data)
        )

        response = json.loads(res.text)

        if res.status_code != 200:
            if 'error' in response and 'message' in response['error']:
                text = '{} \n'.format(response['error']['message'])
                if 'details' in response['error']:
                    for detail in response['error']['details']:
                        if 'field' in detail and 'issue' in detail:
                            text += '{} {} \n'.format(detail['field'], detail['issue'])
                raise models.ValidationError(text)
            raise models.ValidationError(res.text)

        self.dte_base64_data = 'data:application/pdf;base64,{}'.format(response['PDF'])
        self.dte_folio = response['FOLIO']

        return super(AccountInvoice, self).action_invoice_open()
