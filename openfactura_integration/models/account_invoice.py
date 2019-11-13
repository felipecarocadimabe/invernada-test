from odoo import models, fields, api
import requests


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

    def action_invoice_open(self):
        raise models.ValidationError(self.company_id.partner_id.invoice_rut)
        data = {
            'response': [
                'PDF', 'FOLIO'
            ],
            "dte": {
                "Encabezado": {
                    "IdDoc": {
                        "TipoDTE": self.dte_type_id.code,
                        "Folio": 0,
                        "FchEmis": self.date_invoice,
                        "TpoTranCompra": "1",
                        "TpoTranVenta": "1",
                        "FmaPago": self.dte_payment_mode_id.code

                    },
                    "Emisor": {
                        "RUTEmisor": self.partner_id.invoice_rut,
                        "RznSoc": "HAULMER SPA",
                        "GiroEmis": "VENTA AL POR MENOR POR CORREO, POR INTERNET Y VIA TELEFONICA",
                        "Acteco": "479100",
                        "DirOrigen": "ARTURO PRAT 527   CURICO",
                        "CmnaOrigen": "Curicó",
                        "Telefono": "0 0",
                        "CdgSIISucur": "81303347"

                    },
                    "Receptor": {
                        "RUTRecep": "76430498-5",
                        "RznSocRecep": "HOSTY SPA",
                        "GiroRecep": "ACTIVIDADES DE CONSULTORIA DE INFORMATIC",
                        "DirRecep": "ARTURO PRAT 527 3 pis OF 1",
                        "CmnaRecep": "Curicó"

                    },
                    "Totales": {
                        "MntNeto": 2000,
                        "TasaIVA": "19",
                        "IVA": 380,
                        "MntTotal": 2380,
                        "MontoPeriodo": 2380,
                        "VlrPagar": 2380
                    }
                },
                "Detalle": [
                    {
                        "NroLinDet": 1,
                        "NmbItem": "item",
                        "QtyItem": 1,
                        "PrcItem": 2000,
                        "MontoItem": 2000

                    }
                ]
            }
        }
        return super(AccountInvoice, self).action_invoice_open()
