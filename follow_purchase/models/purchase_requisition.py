from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def create(self, vals_list):
        channel = self.env.ref('follow_purchase.channel_purchase_requisition_record')

        if channel:
            vals_list['message_channel_ids'] = [(4, channel.id)]

        item = super(PurchaseRequisition, self).create(vals_list)

        if channel:
            item.write({
                'message_channel_ids': [(4, channel.id)]
            })

        raise models.ValidationError(self.env['purchase.requisition'].search([('id', '=', item.id)]).message_channel_ids)

        return item
