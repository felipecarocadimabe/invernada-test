from odoo import models, fields, api
import datetime


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    exchange_rate = fields.Float(
        'Taza de Cambio'
    )

    @api.model
    @api.onchange('date_invoice')
    def _default_exchange_rate(self):
        date = self.date_invoice
        if date:
            currency_id = self.env['res.currency'].search([('name', '=', 'USD')])
            rate = currency_id.rate_ids.search([('name', '=', date)])
            try:
                rate.ensure_one()
                self.exchange_rate = 1 / rate.rate
            except:
                self.exchange_rate = 0
        else:
            self.exchange_rate = 0


