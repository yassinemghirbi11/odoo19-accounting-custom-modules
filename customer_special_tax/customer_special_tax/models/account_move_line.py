from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_timbre_fiscal = fields.Boolean(string="Is Timbre Fiscal", default=False)