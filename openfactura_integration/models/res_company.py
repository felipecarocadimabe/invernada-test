from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    api_key = fields.Char('Api Key')

    idempotency_key = fields.Char('Idempotency Key')
