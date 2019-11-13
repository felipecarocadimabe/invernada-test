from odoo import models, fields, api


class DTEPaymentMode(models.Model):
    _name = 'dte.payment.mode'

    code = fields.Char(
        'Código',
        required=True
    )

    mode = fields.Char(
        'Forma',
        required=True
    )

    name = fields.Char(
        'Forma de Pago',
        compute='_get_name',
        store=True
    )

    @api.multi
    @api.depends('code', 'mode')
    def _get_name(self):
        for item in self:
            if item.code and item.mode:
                item.name = '{} {}'.format(item.code, item.mode)
            else:
                item.name = ''
