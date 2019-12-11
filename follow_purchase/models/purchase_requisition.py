from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def create(self, vals_list):

        item = super(PurchaseRequisition, self).create(vals_list)

        raise models.ValidationError(item)

        channel = self.env.ref('follow_purchase.channel_purchase_requisition_record')

        if channel:
            item.message_channel_ids = channel
        return item
