import os

base = r"C:\Program Files\Odoo 19.0.20260220\server\custom_addons\retenue_source\views"
os.makedirs(base, exist_ok=True)

xml = r'''<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <record id="view_account_payment_retenue_tree" model="ir.ui.view">
        <field name="name">account.payment.retenue.tree</field>
        <field name="model">account.payment</field>
        <field name="inherit_id" ref="account.view_account_payment_tree"/>
        <field name="mode">primary</field>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='bank_id']" position="attributes">
                <attribute name="invisible">1</attribute>
            </xpath>
        </field>
    </record>

    <record id="view_account_payment_retenue_form" model="ir.ui.view">
        <field name="name">account.payment.retenue.form</field>
        <field name="model">account.payment</field>
        <field name="inherit_id" ref="account.view_account_payment_form"/>
        <field name="mode">primary</field>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='bank_id']" position="attributes">
                <attribute name="invisible">1</attribute>
            </xpath>
        </field>
    </record>

    <record id="view_account_payment_retenue_search" model="ir.ui.view">
        <field name="name">account.payment.retenue.search</field>
        <field name="model">account.payment</field>
        <field name="inherit_id" ref="account.view_account_payment_search"/>
        <field name="arch" type="xml">
            <field name="journal_id" position="after">
                <field name="type_de_retenue"/>
            </field>
            <xpath expr="//group" position="inside">
                <filter name="group_by_type_retenue" string="Type de retenue"
                        context="{'group_by': 'type_de_retenue'}"/>
            </xpath>
        </field>
    </record>

    <record id="action_account_payments_retenue" model="ir.actions.act_window">
        <field name="name">Retenue a la Source</field>
        <field name="res_model">account.payment</field>
        <field name="view_mode">list,form</field>
        <field name="domain">[('journal_id.name', 'ilike', 'Retenue')]</field>
        <field name="context">{}</field>
        <field name="search_view_id" ref="view_account_payment_retenue_search"/>
        <field name="view_ids" eval="[
            (5, 0, 0),
            (0, 0, {'view_mode': 'list', 'view_id': ref('view_account_payment_retenue_tree')}),
            (0, 0, {'view_mode': 'form', 'view_id': ref('view_account_payment_retenue_form')})
        ]"/>
    </record>

    <menuitem id="menu_action_account_payments_retenue_vendor"
              name="Retenue a la Source"
              parent="account.menu_finance_payables"
              action="action_account_payments_retenue"
              sequence="100"/>

    <menuitem id="menu_action_account_payments_retenue_customer"
              name="Retenue a la Source"
              parent="account.menu_finance_receivables"
              action="action_account_payments_retenue"
              sequence="100"/>

</odoo>'''

path = os.path.join(base, "account_payment_views.xml")
with open(path, "w", encoding="utf-8") as f:
    f.write(xml)

print("Done. File saved to:")
print(path)