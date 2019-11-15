from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    optional_usd = fields.Float(
        'Valor Dollar',
        compute='_get_usd_val'
    )

    @api.model
    def _get_usd_val(self):
        try:
            if len(self.invoice_ids) == 1:
                self.optional_usd = self.invoice_ids.exchange_rate
            else:
                self.optional_usd = len(self.invoice_ids)
        except:
            self.optional_usd = 100

    # @api.model
    # def _compute_amount_field(self):

