# -*- coding: utf-8 -*-
from odoo import models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _search(self, domain, offset=0, limit=None, order=None, **kwargs):
        """Restreint la liste des journaux proposés au champ journal_id
        UNIQUEMENT quand la clé de contexte 'retenue_only_journals' est
        présente (elle n'est envoyée que par l'action du menu
        "Retenue à la source"). Le menu Paiements standard n'envoie
        jamais cette clé : son comportement reste donc strictement
        identique, sans aucune modification de vue.
        """
        if self.env.context.get("retenue_only_journals"):
            domain = list(domain) + [("name", "ilike", "retenue")]
        return super()._search(domain, offset=offset, limit=limit, order=order, **kwargs)
