from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def create(self, vals_list):
        channel = self.env.ref('follow_purchase.channel_purchase_requisition_record')

        item = super(PurchaseRequisition, self).create(vals_list)

        mail_wizard_invite = self.env['mail.wizard.invite']\
            .search([('res_model', '=', 'purchase.requisition'), ('res_id', '=', item.id)])

        raise models.ValidationError(mail_wizard_invite)

        if channel and mail_wizard_invite:
            item.update({
                'message_channel_ids': [(4, channel.id)]
            })

        return item
