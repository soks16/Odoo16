# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")

    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status", copy=False)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    property_id = fields.Many2one("estate.property", string="Property", required=True)

    create_date = fields.Date(string='Create Date', default=fields.Date.today)

    validity = fields.Integer(string='Validity (days)', default=7)

    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', default=fields.Date.today)

    def action_validate_sold(self):
        for rec in self:
            rec.write({'status': 'accepted'})
        return True

    def action_invalidate_sold(self):
        for rec in self:
            rec.write({'status': 'refused'})
        return True

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for res in self:
            if res.create_date and res.validity:
                res.date_deadline = res.create_date + timedelta(days=res.validity)
            else:
                res.date_deadline = False

    def _inverse_date_deadline(self):
        for res in self:
            if res.date_deadline and res.create_date:
                res.validity = (res.date_deadline - res.create_date).days
            else:
                res.validity = False
