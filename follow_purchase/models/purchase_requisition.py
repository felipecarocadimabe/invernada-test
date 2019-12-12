from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def create(self, vals_list):
        channel = self.env.ref('follow_purchase.channel_purchase_requisition_record')

        item = super(PurchaseRequisition, self).create(vals_list)

        if channel:
            item.message_channel_ids = [(6, 0, channel.id)]

        raise models.ValidationError(item.message_channel_ids)

        return item
