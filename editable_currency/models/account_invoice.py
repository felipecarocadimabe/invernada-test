from odoo import models, fields, api
import datetime


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    exchange_rate = fields.Float(
        'Taza de Cambio',
        compute='_default_exchange_rate',
        store=True
    )

    @api.model
    @api.depends('date_invoice')
    def _default_exchange_rate(self):
        date = self.date_invoice
        if date:
            currency_id = self.env['res.currency'].search([('name', '=', 'USD')])
            rate = currency_id.rate_ids.search([('name', '=', date)])
            rate.ensure_one()
            return 1 / rate.rate
        else:
            return 0


