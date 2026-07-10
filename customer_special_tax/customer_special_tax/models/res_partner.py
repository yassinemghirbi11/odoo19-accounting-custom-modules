from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    special_tax = fields.Boolean(string="Apply Special Tax")
    partner_type = fields.Selection([
        ("customer", "Client"),
        ("vendor", "Fournisseur"),
    ], string="Type de partenaire")