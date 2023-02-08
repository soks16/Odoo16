# -*- coding: utf-8 -*-

from datetime import date, timedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", default="Unknown", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(sring="Postcode")
    date_availability = fields.Date(string="Available From", default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    active = fields.Boolean(string="Active", default=True)
    garden = fields.Boolean(string="Garden")

    garden_area = fields.Integer(string="Garden Area(sqm)")

    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          string="Garden orientation"
                                          , readonly=False)

    state = fields.Selection([('new', 'New'),
                              ('offer_received', 'Offer Received'),
                              ('offer_accepted', 'Offer Accepted'),
                              ('sold', 'Sold'),
                              ('canceled', 'Canceled')], default='new')

    partner_id = fields.Many2one("res.partner", string="Buyer")
    salesman_id = fields.Many2one("res.users", string="Salesman")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")

    offer_ids = fields.One2many("estate.property.offer", 'property_id', string="Estate Offer")

    total_area = fields.Float(compute="_compute_total_area", store=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best offer")

    _sql_constraints = [
        ('check_expected_price', 'check(expected_price <= 0)',
         'The Expected Price must be strictly positive')
    ]
    # def action_do_something(self):
    #     for record in self:
    #         if record.state == 'new':
    #             record.action_sold()
    #         else:
    #             raise UserError("A cancelled property cannot be set as sold, and a sold property cannot be cancelled.")
    #

    def action_cancel(self):
        for rec in self:
            if rec.state == 'new':
                rec.ensure_one()
                rec.state = 'cancelled'
            elif rec.state == 'sold':
                raise UserError(_("Sold property cannot be cancelled"))
        return True

    def action_sold(self):
        for rec in self:
            if rec.state == 'cancelled':
                raise UserError(_("Cancelled property cannot be sold"))
            else:
                rec.ensure_one()
                rec.state = 'sold'
        return True

    @api.onchange('garden')
    def _change_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_area = 10.0
                rec.garden_orientation = 'north'
            else:
                rec.total_area = rec.garden_area - rec.garden_area
                rec.garden_area = 0
                rec.garden_orientation = ''

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            best_price = [0]
            for rec in record.offer_ids:
                best_price.append(rec.price)
            record.best_price = max(best_price)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.constrains('selling_price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise UserError(_("Selling price must be greater than 0."))
