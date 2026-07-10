from odoo import models, fields

class TunisianBank(models.Model):
    _name = "tunisian.bank"
    _description = "Tunisian Banks"

    name = fields.Char(string="Bank Name", required=True)
    code = fields.Char(string="Bank Code")
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "Bank name must be unique."),
    ]