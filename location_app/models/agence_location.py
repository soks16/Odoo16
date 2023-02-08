# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Salle(models.Model):
    _name = 'agence.salle'
    _description = 'Salle'

    name = fields.Char('Désignation', required=True)
    isactif = fields.Boolean('Active ?')
    nbplaces = fields.Integer('Nombre de place')
    prix_location = fields.Float('Prix Location / Heure :')
    description = fields.Text('Description')


class Bureau(models.Model):
    _name = 'agence.bureau'
    _description = 'Bureau'

    name = fields.Char('Désignation', required=True)
    isactif = fields.Boolean('Actif?')
    surface = fields.Integer('Surface en M2 ')
    prix_location = fields.Float('Prix Location / Mois ')
    description = fields.Text('Description')
