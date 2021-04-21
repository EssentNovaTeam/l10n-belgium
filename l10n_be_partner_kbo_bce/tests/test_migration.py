# Copyright 2021 Essent BE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.modules.migration import load_script
from odoo.tests.common import TransactionCase


class TestMigration(TransactionCase):
    def setUp(self):
        super(TestMigration, self).setUp()
        self.rp_1 = self.env.ref("l10n_be_partner_kbo_bce.res_partner_1")
        self.be = self.env.ref("base.be")
        self.env.cr.execute(
            """
            ALTER TABLE res_partner
            ADD COLUMN registry_number VARCHAR,
            ADD COLUMN registry_authority VARCHAR;
            UPDATE res_partner
            SET registry_number = '0820.512.013',
                registry_authority = 'kbo_bce'
            WHERE id = %s
            """,
            (self.rp_1.id,),
        )

    def test_migration(self):
        """
        Test the custom migration from distinct 8.0 columns to
        res.partner.id_number records
        """
        mod = load_script(
            "l10n_be_partner_kbo_bce/migrations/14.0.1.0.0/post-migration.py",
            "post-migration",
        )
        mod.migrate(self.env.cr, "13.0.1.0.0")
        self.rp_1.refresh()
        self.assertEqual(self.rp_1.kbo_bce_number, "0820.512.013")
