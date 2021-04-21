# Copyright 2021 Essent BE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from openupgradelib import openupgrade


def migrate(cr, version):
    """
    Custom: migrate from distinct 8.0 columns to res.partner.id_number records
    as defined in partner_identification.
    """
    if not version:
        return
    if not (
        openupgrade.column_exists(cr, "res_partner", "registry_number")
        and openupgrade.column_exists(cr, "res_partner", "registry_authority")
    ):
        return
    logger = logging.getLogger("odoo.addons.l10n_be_partner_kbo_bce.migrations")
    logger.info("Migrating kbo_bce numbers")
    cr.execute(
        """
        INSERT INTO res_partner_id_number (
            active,
            category_id,
            create_date,
            create_uid,
            name,
            partner_id
        )
        SELECT
            TRUE,
            (SELECT res_id FROM ir_model_data
             WHERE module = 'l10n_be_partner_kbo_bce'
                 AND name = 'l10n_be_kbo_bce_number_category'),
            NOW() AT TIME ZONE 'UTC',
            1,
            rp.registry_number,
            rp.id
        FROM res_partner rp
        WHERE registry_number IS NOT NULL
            AND registry_number != ''
            AND registry_authority = 'kbo_bce'
        """
    )
    logger.info("Done migrating kbo_bce numbers for %s partners", cr.rowcount)
