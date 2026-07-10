# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PosPayment(models.Model):
    _inherit = "pos.payment"

    cheque_numero = fields.Char(string="Numero de cheque", store=True)
    cheque_date_echeance = fields.Date(string="Date d'echeance", store=True)

    partner_id = fields.Many2one(
        "res.partner",
        string="Client",
        related="pos_order_id.partner_id",
        store=False,
        readonly=True,
    )

    @api.constrains("cheque_numero")
    def _check_cheque_numero_digits(self):
        for payment in self:
            if payment.cheque_numero and not re.match(r"^\d+$", payment.cheque_numero):
                raise ValidationError("Le numero de cheque doit contenir uniquement des chiffres.")