from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def create(self, vals_list):

        item = super(PurchaseRequisition, self).create(vals_list)

        channel = self.env.ref('follow_purchase.channel_purchase_requisition_record')

        raise models.ValidationError(vals_list['message_channel_ids'])

        if channel:
            item.message_channel_ids = channel
        return item
