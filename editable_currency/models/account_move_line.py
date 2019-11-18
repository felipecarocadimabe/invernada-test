from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _compute_amount_fields(self, amount, src_currency, company_currency):
        """ Helper function to compute value for fields debit/credit/amount_currency based on an amount and the currencies given in parameter"""

        optional_usd = self.env.context.get('optional_usd') or False
        amount_currency = False
        currency_id = False
        date = self.env.context.get('date') or fields.Date.today()
        company = self.env.context.get('company_id')
        company = self.env['res.company'].browse(company) if company else self.env.user.company_id
        if src_currency and src_currency != company_currency:
            amount_currency = amount
            amount = src_currency.with_context(
                optional_usd=optional_usd
            )._convert(amount, company_currency, company, date)
            currency_id = src_currency.id
        debit = amount > 0 and amount or 0.0
        credit = amount < 0 and -amount or 0.0
        return debit, credit, amount_currency, currency_id

    def _check_reconcile_validity(self):
        # Perform all checks on lines

        company_ids = set()
        all_accounts = []
        for line in self:
            company_ids.add(line.company_id.id)
            all_accounts.append(line.account_id)
            if (line.matched_debit_ids or line.matched_credit_ids) and line.reconciled:
                raise models.ValidationError(_('You are trying to reconcile some entries that are already reconciled.'))
        if len(company_ids) > 1:
            raise models.ValidationError(_('To reconcile the entries company should be the same for all entries.'))
        if len(set(all_accounts)) > 1:
            raise models.ValidationError(all_accounts)
            raise models.ValidationError(_('Entries are not from the same account.'))
        if not (all_accounts[0].reconcile or all_accounts[0].internal_type == 'liquidity'):
            raise models.ValidationError(_(
                'Account %s (%s) does not allow reconciliation. First change the configuration of this account to allow it.') % (
                                             all_accounts[0].name, all_accounts[0].code))


