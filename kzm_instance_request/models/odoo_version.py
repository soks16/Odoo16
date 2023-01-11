from odoo import fields, models


class Odoo_Version(models.Model):
    _name = "odoo.version"
    _description = "odoo version"

    name = fields.Char("version")
