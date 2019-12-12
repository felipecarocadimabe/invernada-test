from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def create(self, vals_list):
        channel = self.env.ref('follow_purchase.channel_purchase_requisition_record')

        item = super(PurchaseRequisition, self).create(vals_list)

        mail_wizard_invite = self.env['mail.wizard.invite'].create({
            'res_model': 'purchase.requisition',
            'res_id': item.id,
            'channel_ids': [(4, channel.id)],
            'message': 'nueva solicitud creada'
        })

        mail_wizard_invite.add_followers()

        return item
