from odoo import models, fields, api, exceptions


class Acteco(models.Model):
    _name = 'acteco'

    code = fields.Char(
        'Código',
        required=True,
        unique=True
    )

    activity = fields.Text(
        'Actividad',
        required=True
    )

    iva_affect = fields.Selection(
        [
            ('yes', 'SI'),
            ('no', 'NO'),
            ('g', 'G'),
        ],
        'Afecto a IVA',
        required=True
    )

    category = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('g', 'G'),
        ],
        'Categoría',
        required=True
    )

    internet_available = fields.Boolean('Disponible Internet')

    @api.model
    def create(self, values):
        acteco = self.env['acteco'].search([('code', '=', values['code'])])

        if acteco is not None:
            raise ValueError(
                'código de acteco ya existe'
                'code'
            )

        return super(Acteco, self).create()
