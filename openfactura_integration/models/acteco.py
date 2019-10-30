from odoo import models, fields


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
