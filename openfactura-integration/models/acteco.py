from odoo import models, fields


class Acteco(models.Model):

    code = fields.Integer(
        'Código',
        required=True,
        unique=True
    )

    description = fields.Text(
        'Actividad',
        required=True
    )

    tax_affect = fields.Selection(
        [
            ('yes', 'SÍ'),
            ('no', 'No'),
            ('g', 'G'),
        ],
        'Afecto a IVA'
    )

    category = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('g', 'G')
        ],
        'Categoría Tributaria'
    )

    internet_available = fields.Boolean('Disponible Internet')
