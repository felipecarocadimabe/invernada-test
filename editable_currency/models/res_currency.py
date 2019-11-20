from odoo import models, fields
import requests
import json


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def _convert(self, from_amount, to_currency, company, date, round=True):

        optional_usd = self.env.context.get('optional_usd') or False

        self, to_currency = self or to_currency, to_currency or self
        assert self, "convert amount from unknown currency"
        assert to_currency, "convert amount to unknown currency"
        assert company, "convert amount from unknown company"
        assert date, "convert amount from unknown date"
        # apply conversion rate
        if self == to_currency:
            to_amount = from_amount
        else:
            exchange = self._get_conversion_rate(self, to_currency, company, date)
            if optional_usd:
                exchange = 1 / optional_usd
            to_amount = from_amount * exchange

        # apply rounding
        return to_currency.round(to_amount) if round else to_amount

    def get_rate_by_date(self, date):
        res = requests.request(
            'GET',
            'https://services.dimabe.cl/api/currencies?date={}'.format(date.strftime('%Y-%m-%d')),
            headers={
                'apikey': '790AEC76-9D15-4ABF-9709-E0E3DC45ABBC'
            }
        )

        response = json.loads(res.text)

        rate = None

        for data in response:
            if data['currency'] == 'USD':
                rate = float(data['value'])

        raise models.ValidationError(rate)

        if res.status_code == 200:
            self.env['res.currency.rate'].create({
                'name': date,
                'rate': rate,
                'currency_id': self.id
            })
