from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def create(self, vals_list):
        channel = self.env.ref('follow_purchase.channel_purchase_requisition_record')
        if channel:
            vals_list['message_channel_ids'] = (6, 0, channel)
        item = super(PurchaseRequisition, self).create(vals_list)

        raise models.ValidationError(item.message_channel_ids)

        return item
