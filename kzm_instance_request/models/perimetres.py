from odoo import fields, models


class Perimetre(models.Model):
    _name = "odoo.perimeter"
    _description = "perimetres"

    name = fields.Char(string="Name")

