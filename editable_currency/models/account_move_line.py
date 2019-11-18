from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _compute_amount_fields(self, amount, src_currency, company_currency):

        raise models.ValidationError('{} _compute_amount_field'.format(self.env.context.get('optional_usd') or False))

        debit, credit, amount_currency, currency_id = super(AccountMoveLine, self)._compute_amount_fields(amount, src_currency, company_currency)

        raise models.ValidationError(self.invoice_id.id)

        raise models.ValidationError('{} - {} - {} - {}'.format(debit, credit, amount_currency, currency_id))

