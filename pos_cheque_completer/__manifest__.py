# -*- coding: utf-8 -*-
{
    "name": "POS Cheque a Completer",
    "version": "1.0",
    "author": "Custom",
    "category": "Point of Sale",
    "summary": "Menu pour completer les numeros et dates d'echeance des cheques POS",
    "depends": ["point_of_sale", "journal_payment_fields"],
    "data": [
        "security/ir.model.access.csv",
        "views/pos_payment_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}