from odoo import models, fields

class AccountTax(models.Model):
    _inherit = "account.tax"

    retenue = fields.Boolean(string="Retenue")