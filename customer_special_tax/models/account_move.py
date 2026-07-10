from odoo import models, fields, api

STAMP_TAX_NAME = "1DT TS"

class AccountMove(models.Model):
    _inherit = "account.move"

    apply_stamp_tax = fields.Boolean(
        compute="_compute_apply_stamp_tax",
        store=False,
    )

    @api.depends("partner_id")
    def _compute_apply_stamp_tax(self):
        for move in self:
            move.apply_stamp_tax = bool(
                move.partner_id and move.partner_id.commercial_partner_id.special_tax
            )

    def _get_stamp_tax(self):
        """Find the 1DT TS tax record."""
        return self.env["account.tax"].search([
            ("name", "ilike", STAMP_TAX_NAME),
            ("company_id", "=", self.company_id.id),
        ], limit=1)

    def _apply_stamp_tax(self):
        """Add 1DT TS tax ONLY to the FIRST invoice line when special_tax=True."""
        stamp_tax = self._get_stamp_tax()
        if not stamp_tax:
            return

        for move in self:
            partner = move.partner_id.commercial_partner_id
            lines = move.invoice_line_ids

            if not partner.special_tax:
                # Remove stamp tax from ALL lines
                for line in lines:
                    if stamp_tax in line.tax_ids:
                        line.tax_ids = [(3, stamp_tax.id, 0)]
                continue

            # Remove stamp tax from ALL lines first
            for line in lines:
                if stamp_tax in line.tax_ids:
                    line.tax_ids = [(3, stamp_tax.id, 0)]

            # Add stamp tax ONLY to the FIRST line (lowest sequence)
            if lines:
                first_line = lines.sorted('sequence')[0]
                if stamp_tax not in first_line.tax_ids:
                    first_line.tax_ids = [(4, stamp_tax.id, 0)]

    @api.onchange("partner_id")
    def _onchange_partner_stamp_tax(self):
        self._apply_stamp_tax()

    @api.onchange("invoice_line_ids")
    def _onchange_invoice_line_ids_stamp_tax(self):
        """Re-apply stamp tax whenever invoice lines change."""
        self._apply_stamp_tax()

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        moves._apply_stamp_tax()
        return moves

    def write(self, vals):
        result = super().write(vals)
        if "invoice_line_ids" in vals or "partner_id" in vals:
            self._apply_stamp_tax()
        return result

    def _get_tax_totals(self):
        """Rename stamp tax to 'Timbre Fiscal' in totals display."""
        result = super()._get_tax_totals()
        if not result or not isinstance(result, dict):
            return result

        stamp_name_lower = STAMP_TAX_NAME.lower()
        
        if "groups_by_subtotal" in result:
            for key, groups in result["groups_by_subtotal"].items():
                if isinstance(groups, list):
                    for group in groups:
                        if isinstance(group, dict) and stamp_name_lower in group.get("tax_group_name", "").lower():
                            group["tax_group_name"] = "Timbre Fiscal"
        
        if "subtotals" in result:
            for subtotal in result["subtotals"]:
                if isinstance(subtotal, dict) and "tax_groups" in subtotal:
                    for tg in subtotal["tax_groups"]:
                        if isinstance(tg, dict) and stamp_name_lower in tg.get("tax_group_name", "").lower():
                            tg["tax_group_name"] = "Timbre Fiscal"
        
        return result