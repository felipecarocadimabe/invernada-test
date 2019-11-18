from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    optional_usd = fields.Float(
        'Valor Dollar',
        compute='_get_usd_val'
    )

    @api.one
    @api.depends('invoice_ids')
    def _get_usd_val(self):
        try:
            if len(self.invoice_ids) == 1:
                self.optional_usd = self.invoice_ids.exchange_rate
            else:
                self.optional_usd = 0
        except:
            self.optional_usd = 0

    def action_validate_invoice_payment(self):

        return super(
            AccountPayment,
            self.with_context(optional_usd=self.optional_usd)
        ).action_validate_invoice_payment()

    def post(self):
        raise models.ValidationError(self._context.get('optional_usd', False))
