from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    check_list_responses = fields.One2many(
        'check.list.response',
        'picking_id',
        'Check List'
    )

    has_mp_field = fields.Boolean(
        'tiene campo mp',
        compute='_compute_has_mp_field'
    )

    @api.model
    def create(self, val_list):
        items = self.get_all_check_list_items()

        picking = super(StockPicking, self).create(val_list)

        responses = []
        for item in items:
            responses.append({
                'item': item.id,
                'picking_id': picking.id
            })

        self.env['check.list.response'].create(responses)

        return picking

    @api.model
    def get_all_check_list_items(self):
        items = self.env['check.list.item']
        return items.search([])

    @api.multi
    def _compute_has_mp_field(self):
        for item in self:
            if 'is_mp_reception' in item.env['stock.picking']._fields:
                item.has_mp_field = True
            else:
                item.has_mp_field = False
