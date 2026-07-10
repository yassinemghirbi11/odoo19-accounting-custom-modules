from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = "account.journal"

    payment_type = fields.Selection([
        ("cheque", "Cheque"),
        ("traite", "Traite"),
        ("virement", "Virement"),
    ], string="Type de paiement")

    date_echeance = fields.Date(string="Date d'echeance")
    bank_name = fields.Char(string="Nom de la banque")
    bank_code = fields.Char(string="Code banque")
    numero_cheque = fields.Char(string="Numero de cheque")
    numero_traite = fields.Char(string="Numero de traite")

    partner_type = fields.Selection([
        ("customer", "Client"),
        ("vendor", "Fournisseur"),
    ], string="Type de partenaire")

    customer_id = fields.Many2one(
        "res.partner",
        string="Client",
        domain="[('customer_rank', '>', 0), ('parent_id', '=', False)]",
    )

    vendor_id = fields.Many2one(
        "res.partner",
        string="Fournisseur",
        domain="[('supplier_rank', '>', 0), ('parent_id', '=', False)]",
    )