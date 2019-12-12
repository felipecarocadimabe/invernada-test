from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class PurchaseRequisition(models.Model):
    _inherit = ['purchase.requisition']

    @api.model
    def create(self, vals_list):
        channel = self.env.ref('follow_purchase.channel_purchase_requisition_record')

        item = super(PurchaseRequisition, self).create(vals_list)

        mail_wizard_invite = self.env['mail.wizard.invite'].create({
            'res_model': 'purchase.requisition',
            'res_id': item.id,
            'channel_ids': [(4, channel.id)],
        })

        mail_wizard_invite.add_followers()

        mail_wizard_invite.message_post(body='lala pc')

        return item

    @api.multi
    def action_in_progress(self):
        self.ensure_one()
        self.message_ids = [(0, 0, {'body': 'lala pc', 'message_type': 'notification'})]
        raise models.ValidationError(self.message_ids)
