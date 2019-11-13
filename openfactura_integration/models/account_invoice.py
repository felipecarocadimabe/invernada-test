from odoo import models, fields, api


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

