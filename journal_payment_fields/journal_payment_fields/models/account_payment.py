from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountPayment(models.Model):
    _inherit = "account.payment"

    payment_type_custom = fields.Selection([
        ("cheque", "Cheque"),
        ("traite", "Traite"),
        ("virement", "Virement"),
    ], string="Type de paiement")

    date_echeance = fields.Date(string="Date d'echeance")
    numero_cheque = fields.Char(string="Numero de cheque")
    numero_traite = fields.Char(string="Numero de traite")

    bank_id = fields.Many2one(
        "tunisian.bank",
        string="Bank",
        help="Select the bank for this payment",
    )

    # Base domain: only taxes with retenue=True
    # Onchange adds type_tax_use filter dynamically
    type_de_retenue = fields.Many2one(
        "account.tax",
        string="Type de retenue",
        domain="[('retenue', '=', True)]",
        help="Select the retenue tax type",
    )

    pourcentage = fields.Float(
        string="Percentage (Deprecated)",
        default=0.0,
        store=False,
    )

    show_retenue = fields.Boolean(
        string="Show Retenue",
        compute="_compute_show_retenue",
        store=False,
    )

    montant_retenue = fields.Monetary(
        string="Montant Retenue",
        compute="_compute_montant_retenue",
        store=False,
        currency_field="currency_id",
    )

    is_retenue_journal = fields.Boolean(
        string="Is Retenue Journal",
        compute="_compute_is_retenue_journal",
        store=False,
    )

    @api.depends("journal_id")
    def _compute_is_retenue_journal(self):
        for pay in self:
            pay.is_retenue_journal = bool(
                pay.journal_id and "retenue" in (pay.journal_id.name or "").lower()
            )

    @api.depends("journal_id", "amount")
    def _compute_show_retenue(self):
        for pay in self:
            if "retenue" not in self.env["account.tax"]._fields:
                pay.show_retenue = False
                continue
            retenue_tax = self.env["account.tax"].search([
                ("retenue", "=", True),
                ("type_tax_use", "=", "sale"),
            ], limit=1)
            retenue_journal = self.env["account.journal"].search([
                ("name", "ilike", "Retenue"),
            ], limit=1)
            pay.show_retenue = bool(
                retenue_tax and retenue_journal and pay.journal_id == retenue_journal
            )

    @api.depends("amount", "type_de_retenue", "is_retenue_journal")
    def _compute_montant_retenue(self):
        for pay in self:
            if pay.is_retenue_journal and pay.type_de_retenue:
                pay.montant_retenue = pay.amount * (pay.type_de_retenue.amount / 100.0)
            else:
                pay.montant_retenue = 0.0

    @api.onchange("journal_id")
    def _onchange_journal_auto_payment_type(self):
        if self.journal_id:
            journal_name = (self.journal_id.name or "").lower()
            if "cheque" in journal_name:
                self.payment_type_custom = "cheque"
            elif "traite" in journal_name or "trait" in journal_name:
                self.payment_type_custom = "traite"
            elif "virement" in journal_name or "bank" in journal_name:
                self.payment_type_custom = "virement"

    @api.onchange("journal_id")
    def _onchange_journal_clear_retenue_type(self):
        if not self.is_retenue_journal:
            self.type_de_retenue = False

    @api.onchange("payment_type")
    def _onchange_payment_type_retenue_domain(self):
        self.type_de_retenue = False
        if self.payment_type == "inbound":
            # Customer (Receive) → Sales taxes
            return {"domain": {"type_de_retenue": [("retenue", "=", True), ("type_tax_use", "=", "sale")]}}
        else:
            # Vendor (Send) → Purchase taxes
            return {"domain": {"type_de_retenue": [("retenue", "=", True), ("type_tax_use", "=", "purchase")]}}

    @api.onchange("partner_type")
    def _onchange_partner_type_domain(self):
        if self.partner_type == "customer":
            return {"domain": {"partner_id": [("partner_type_id.name", "=", "Client"), ("parent_id", "=", False)]}}
        elif self.partner_type == "supplier":
            return {"domain": {"partner_id": [("partner_type_id.name", "=", "Fournisseur"), ("parent_id", "=", False)]}}

    def _compute_available_journal_ids(self):
        super()._compute_available_journal_ids()
        retenue = self.env["account.journal"].search([("name", "ilike", "Retenue")])
        if retenue:
            for pay in self:
                pay.available_journal_ids = pay.available_journal_ids | retenue

    def _set_payment_method_for_retenue(self):
        for pay in self:
            if not pay.payment_method_line_id:
                if pay.payment_type == "inbound":
                    lines = pay.journal_id.inbound_payment_method_line_ids
                else:
                    lines = pay.journal_id.outbound_payment_method_line_ids
                if lines:
                    pay.payment_method_line_id = lines[0]

    @api.onchange("journal_id")
    def _onchange_journal_set_payment_method(self):
        if self.is_retenue_journal:
            self._set_payment_method_for_retenue()

    @api.model_create_multi
    def create(self, vals_list):
        payments = super().create(vals_list)
        payments._set_payment_method_for_retenue()
        return payments

    def write(self, vals):
        res = super().write(vals)
        if "journal_id" in vals or "payment_type" in vals:
            self._set_payment_method_for_retenue()
        return res

    @api.constrains("amount")
    def _check_amount_required(self):
        for pay in self:
            if pay.amount <= 0:
                raise ValidationError("Amount must be greater than 0.")

    @api.constrains("payment_type_custom", "numero_cheque", "numero_traite", "date_echeance")
    def _check_payment_details_required(self):
        for pay in self:
            if pay.payment_type_custom == "cheque":
                if not pay.numero_cheque:
                    raise ValidationError("Numero de cheque is required for cheque payments.")
                if not pay.date_echeance:
                    raise ValidationError("Date d'echeance is required for cheque payments.")
            elif pay.payment_type_custom == "traite":
                if not pay.numero_traite:
                    raise ValidationError("Numero de traite is required for traite payments.")
                if not pay.date_echeance:
                    raise ValidationError("Date d'echeance is required for traite payments.")