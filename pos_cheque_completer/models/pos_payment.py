# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PosPayment(models.Model):
    _inherit = "pos.payment"

    cheque_numero = fields.Char(string="Numero de cheque", store=True)
    cheque_date_echeance = fields.Date(string="Date d'echeance", store=True)
    proprietaire = fields.Char(string="Proprietaire", store=True)
    note = fields.Text(string="Note", store=True)

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

    def write(self, vals):
        res = super().write(vals)
        if "cheque_numero" in vals or "cheque_date_echeance" in vals:
            self._sync_cheque_to_account_payment()
        return res

    def _sync_cheque_to_account_payment(self):
        """Push cheque_numero / cheque_date_echeance onto the linked
        account.payment (via account_move_id -> account.move.payment_ids),
        so the fields added by journal_payment_fields (numero_cheque,
        date_echeance) are filled automatically, and the payment type
        is set to 'cheque' so the checkbox/radio reflects it too."""
        for pos_pay in self:
            if not pos_pay.account_move_id:
                continue
            move = pos_pay.account_move_id
            payments = move.payment_ids
            if not payments:
                continue

            update_vals = {}
            if pos_pay.cheque_numero:
                update_vals["numero_cheque"] = pos_pay.cheque_numero
            if pos_pay.cheque_date_echeance:
                update_vals["date_echeance"] = pos_pay.cheque_date_echeance
            if update_vals:
                # Mark it as a cheque payment so the "Cheque" radio/checkbox
                # is ticked and the conditional fields become visible/required.
                if "payment_type_custom" in payments._fields:
                    update_vals["payment_type_custom"] = "cheque"
                payments.write(update_vals)