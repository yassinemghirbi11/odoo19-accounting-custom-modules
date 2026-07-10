from odoo import models, fields

class ResPartnerType(models.Model):
    _name = "res.partner.type"
    _description = "Partner Type"
    _order = "name"

    name = fields.Char(string="Type", required=True)
    active = fields.Boolean(default=True)