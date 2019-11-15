from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    optional_usd = fields.Float(
        'Valor Dollar',
        compute=''
    )

    # @api.model
    # def _compute_amount_field(self):

