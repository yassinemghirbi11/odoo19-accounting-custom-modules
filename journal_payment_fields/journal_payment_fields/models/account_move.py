from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange("move_type")
    def _onchange_move_type_partner_domain(self):
        if self.move_type in ("out_invoice", "out_refund"):
            return {"domain": {"partner_id": [("partner_type_id.name", "=", "Client")]}}
        elif self.move_type in ("in_invoice", "in_refund"):
            return {"domain": {"partner_id": [("partner_type_id.name", "=", "Fournisseur")]}}
        return {}