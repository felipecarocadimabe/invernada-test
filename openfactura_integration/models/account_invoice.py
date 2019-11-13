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
    #{
    #    "RUTEmisor": self.company_id.partner_id.invoice_rut,
    #    "RznSoc": self.company_id.partner_id.name,
    #    "GiroEmis": self.company_id.partner_id.acteco_id.activity,
    #    "Acteco": self.company_id.partner_id.acteco_id.code,
    #    "DirOrigen": self.company_id.partner_id.street,
    #    "CmnaOrigen": self.company_id.partner_id.city,
    #    "Telefono": self.company_id.partner_id.phone,
    #    "CdgSIISucur": self.company_id.partner_id.branch_office_sii_code
    #}
    #{
    #    "RUTRecep": self.partner_id.invoice_rut,
    #    "RznSocRecep": self.partner_id.name,
    #    "GiroRecep": self.partner_id.acteco_id.activity,
    #    "DirRecep": self.partner_id.street,
    #    "CmnaRecep": self.partner_id.city
    #}

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
        return json.dumps(lines)

    def action_invoice_open(self):

        emitter = self.company_id.partner_id.get_emitter_data()
        receiver = self.partner_id.get_receiver_data()
        detail = self.get_detail_data()
        data = {
            'response': [
                'PDF', 'FOLIO'
            ],
            'dte': {
                'Encabezado': {
                    'IdDoc': {
                        'TipoDTE': self.dte_type_id.code,
                        'Folio': 0,
                        'FchEmis': self.date_invoice,
                        'TpoTranCompra': "1",
                        'TpoTranVenta': "1",
                        'FmaPago': self.dte_payment_mode_id.code

                    },
                    'Emisor': emitter,
                    'Receptor': receiver,
                    'Totales': {
                        'MntNeto': self.amount_untaxed,
                        'TasaIVA': "19",
                        'IVA': self.amount_tax,
                        'MntTotal': self.amount_total,
                        'MontoPeriodo': self.amount_total,
                        'VlrPagar': self.amount_total
                    }
                },
                'Detalle': detail
            }
        }
        raise models.ValidationError(self.dte_type_id.code)
        raise models.ValidationError(json.dumps(data))
        res = requests.request(
            'POST',
            'https://dev-api.haulmer.com/v2/dte/document',
            headers={
                'apikey': self.company_id.api_key
            },
            data=json.dumps(data)
        )

        raise models.ValidationError(res.text)

        return super(AccountInvoice, self).action_invoice_open()
