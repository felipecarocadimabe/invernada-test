from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    optional_usd = fields.Float(
        'Valor Dollar',
        default=lambda self: self._get_usd_val()
    )

    @api.model
    def _get_usd_val(self):
        try:
            if len(self.invoice_ids) == 1:
                return self.invoice_ids.exchange_rate
            else:
                return 200
        except:
            return 100


    # @api.model
    # def _compute_amount_field(self):

