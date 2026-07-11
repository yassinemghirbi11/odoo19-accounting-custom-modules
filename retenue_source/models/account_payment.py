# -*- coding: utf-8 -*-
from odoo import models, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get("retenue_only_journals") and "journal_id" in fields_list:
            journal = self.env["account.journal"].search(
                [("name", "ilike", "retenue")], limit=1
            )
            if journal:
                res["journal_id"] = journal.id
        return res