from odoo import models, fields, api


class Acteco(models.Model):
    _name = 'acteco'

    _sql_constraints = [
        ('code', 'unique(code)', 'el código ya se encuentra en el listado')
    ]

    name = fields.Char(
        'acteco',
        compute='_get_name',
        store=True
    )

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

        if values['activity'] is not None:
            values['activity'] = str(values['activity']).upper()

        return super(Acteco, self).create(values)

    @api.multi
    def write(self, values):

        if values['activity'] is not None:
            values['activity'] = str(values['activity']).upper()

        return super(Acteco, self).write(values)

    @api.multi
    @api.depends('code', 'activity')
    def _get_name(self):
        for item in self:
            item.name = '{} - {}'.format(item.code, item.activity)
