from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(hes_number)', 'el número ya se encuentra en el sistema')
    ]

    hes_number = fields.Integer(
        'Hoja de entrega de servicio',
        nullable=True,
        default=None,
        readonly=True
    )

    hes_sent_count = fields.Integer(
        'Veces Enviado',
        default=0,
        readonly=True
    )

    @api.multi
    def send_hes(self):
        template_id = self.env.ref('reception_check.hes_mail_template')
        self.message_post_with_template(template_id.id)
        self.sum_send_hes()

    @api.returns('self')
    def generate_hes(self):
        self.ensure_one()

        if self.hes_number is None:
            self.hes_number = self.env['purchase.order'].search([])[-1].hes_number + 1

        return self

    @api.returns('self')
    def sum_send_hes(self):
        self.ensure_one()
        self.hes_sent_count = self.hes_sent_count + 1
        return self

