# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Employee(models.Model):
    _inherit = 'hr.employee'

    instance_ids = fields.One2many(comodel_name='kzm.instance.request', inverse_name='tl_id', string="Instance",
                                   tracking=True)
    nbre_instance_ids = fields.Integer(string='Instance count', compute='comp_nbre_instance')

    @api.depends('instance_ids')
    def comp_nbre_instance(self):
        for x in self:
            x.nbre_instance_ids = len(x.instance_ids)

    def action_instances(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Instances',
            'res_model': 'kzm.instance.request',
            'domain': [('tl_id', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
