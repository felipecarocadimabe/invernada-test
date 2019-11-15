from odoo import models, fields, api
import datetime


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    exchange_rate = fields.Float(
        'Taza de Cambio',
        default=lambda self: self._default_exchange_rate()
    )

    @api.model
    def _default_exchange_rate(self):
        date = self.date_invoice
        raise models.ValidationError(str(date))
        if not date:
            date = datetime.date.today()
        currency_id = self.env['res.currency'].search([('name', '=', 'USD')])
        rate = currency_id.rate_ids.search([('name', '=', date)])
        rate.ensure_one()
        return 1 / rate.rate


