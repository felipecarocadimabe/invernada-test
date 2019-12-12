from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


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
        })

        _logger.error(item.message_ids[0])

        raise models.ValidationError(item.message_ids)
        # schannel.message_ids

        mail_wizard_invite.add_followers()

        return item
