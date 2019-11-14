from odoo import models, fields, api
import requests
import json


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    dte_type_id = fields.Many2one(
        'dte.type',
        'Tipo de Factura',
        required=True
    )

    dte_payment_mode_id = fields.Many2one(
        'dte.payment.mode',
        'Forma de Pago',
        required=True
    )

    dte_base64_data = fields.Text(
        'Documento PDF'
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
                        'TasaIVA': "19",
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

        #if res.status_code != 200:
        response = json.loads(res.text)
        raise models.ValidationError(response['PDF'])

        self.dte_base64_data = 'data:application/pdf;base64,{}'.format(response['PDF'])

        return super(AccountInvoice, self).action_invoice_open()
