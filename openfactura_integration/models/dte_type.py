from odoo import models, fields, api


class DTEType(models.Model):
    _name = 'dte.type'
    _sql_constraints = [
        ('unique_id', 'UNIQUE(code)', 'el código ya se encuentra en el sistema')
    ]

    name = fields.Char(
        'Tipo',
        compute='_get_name',
        store=True
    )

    code = fields.Integer(
        'Código',
        required=True
    )

    dte_type = fields.Char(
        'Tipo DTE',
        required=True
    )

    @api.multi
    @api.depends('code', 'dte_type')
    def _get_name(self):
        for item in self:
            if item.dte_type and item.code:
                item.name = '{} {}'.format(str(item.code), item.dte_type)
            else:
                item.name = ''
