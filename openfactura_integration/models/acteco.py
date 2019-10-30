from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Acteco(models.Model):
    _name = 'acteco'

    _sql_constraints = [
        ('code', 'unique(code)', 'el código ya se encuentra en el listado')
    ]

    code = fields.Char(
        'Código',
        required=True,
        unique=True
    )

    activity = fields.Text(
        'Actividad',
        required=True,
        compute='_to_upper'
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

    @api.onchange('activity')
    @api.model
    def _to_upper(self):
        self.activity = str.upper(self.activity)

#    @api.model
#    def create(self, values):
#        acteco = self.env['acteco'].search([('code', '=', values['code'])])

#        if acteco is not None:
#            raise ValidationError(
#                'código de acteco ya existe'
#            )VENTA AL POR MENOR EN EMPRESAS DE VENTA A DISTANCIA VÍA INTERNET; COMERCIO ELEC

#        return super(Acteco, self).create()
