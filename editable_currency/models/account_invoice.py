from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    exchange_rate = fields.Float(
        'Taza de Cambio',
        default=lambda self: self._default_exchange_rate()
    )

    @api.model
    def _default_exchange_rate(self):

        return 700

