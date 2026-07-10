{
    "name": "Journal Payment Fields",
    "version": "1.2",
    "author": "Your Company",
    "category": "Accounting",
    "depends": ["account", "base"],
    "data": [
        "security/ir.model.access.csv",
        "data/tunisian_bank_data.xml",
        "views/account_payment_view.xml",
        "views/account_payment_retenue_views.xml",
        "views/account_journal_view.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "journal_payment_fields/static/src/css/hide_bank_account.css"
        ]
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}