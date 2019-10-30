from odoo import models, fields


class Acteco(models.Model):

    code = fields.Integer('Código')

    activity = fields.Text('Actividad')

    iva_affect = fields.Selection(
        [
            ('yes', 'SI'),
            ('no', 'NO'),
            ('g', 'G'),
        ],
        'Afecto a IVA'
    )

    category = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('g', 'G'),
        ],
        'Categoría'
    )

    internet_available = fields.Boolean('Disponible Internet')
