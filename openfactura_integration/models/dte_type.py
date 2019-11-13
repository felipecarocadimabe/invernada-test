from odoo import models, fields, api


class DTEType(models.Model):
    _name = 'dte.type'

    name = fields.Char(
        'Tipo',
        compute='_get_name',
        store=True,
        invisible=True
    )

    code = fields.Char('Código')

    dte_type = fields.Char('Tipo DTE')

    @api.multi
    @api.depends('code', 'dte_type')
    def _get_name(self):
        for item in self:
            item.name = '{} {}'.format(item.code, item.dte_type)
