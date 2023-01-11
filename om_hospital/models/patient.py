# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    ref = fields.Char(string="Reference")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
