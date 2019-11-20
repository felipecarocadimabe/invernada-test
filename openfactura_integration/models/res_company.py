from odoo import models, fields
import requests
import json


class ResCompany(models.Model):
    _inherit = 'res.company'

    api_key = fields.Char('Api Key')

    idempotency_key = fields.Char('Idempotency Key')

    def sync_received_invoice(self):
        res = requests.request(
            'POST',
            'https://dev-api.haulmer.com/v2/dte/document/received',
            headers={
                'apikey': self.api_key
            }
        )

        response = json.loads(res.text)

        raise models.ValidationError(res.text)

        if res.status_code != 200:
            raise models.ValidationError(res.text)
