# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class OdooVersion(models.Model):
    _inherit = 'odoo.version'

    instance_ids = fields.One2many('kzm.instance.request', inverse_name='odoo_id', string="Instance")
    nbre_instance_ids = fields.Integer(string='Instance count', compute='comp_nbre_instance')

    @api.depends('instance_ids')
    def comp_nbre_instance(self):
        for x in self:
            x.nbre_instance_ids = len(x.instance_ids)
