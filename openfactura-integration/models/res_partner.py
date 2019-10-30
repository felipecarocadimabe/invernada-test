from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    business_turn = fields.Char(
        'Giro Empresaa'
    )
