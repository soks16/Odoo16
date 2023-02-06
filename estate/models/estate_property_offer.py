# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"

    price = fields.Float(string="Price")

    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="State", copy=False)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    property_id = fields.Many2one("estate.property", string="Property", required=True)
