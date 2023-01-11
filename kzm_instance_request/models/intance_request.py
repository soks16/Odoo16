# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import timedelta, date, datetime
from odoo.exceptions import ValidationError


class Instance_Request(models.Model):
    _name = "kzm.instance.request"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = "creation d'instance"

    name = fields.Char(string="Designation", tracking=True)
    reference = fields.Char(string="Order Reference",
                            required=True, copy=False,
                            default=lambda self: _('New'))
    active = fields.Boolean(default=True)
    adress_ip = fields.Char(string="Address IP")
    cpu = fields.Char(string="CPU")
    ram = fields.Char(string="RAM")
    disk = fields.Char(string="DISK")
    url = fields.Char(string="URL")
    current_time = fields.Datetime.now()
    state = fields.Selection(
        selection=[('brouillon', 'Draft copy'), ('soumise', 'Submissive'), ('entraitement', 'Processing'),
                   ('traite', 'Processed')],
        default='brouillon', tracking=True)
    limit_date = fields.Date(tracking=True)
    treat_date = fields.Datetime()
    treat_duration = fields.Integer(string="Treat Duration", compute="comp_duration", store=True)
    sale_id = fields.Many2one(comodel_name='sale.order', string="Sale order")

    _sql_constraints = [
        ('adresse_ip_unique',
         'unique (adress_ip)',
         "Please enter a unique ip address, the given address already exists !")
    ]

    partner_id = fields.Many2one(string="Customer", comodel_name='res.partner')
    tl_id = fields.Many2one(string="Employees", comodel_name='hr.employee')
    tl_user_id = fields.Many2one(string="Employee", comodel_name='res.users')
    odoo_id = fields.Many2one(string="Odoo version", comodel_name='odoo.version')
    perimeters_ids = fields.Many2many(string="Perimeters", comodel_name='odoo.perimeter')
    # address_employee = fields.Many2one(string="Address employee", related='employee_id.address_id')

    nbre_perimeter = fields.Float(string="Number of perimeters", compute='comp_perimeter', store=True)

    @api.depends('perimeters_ids')
    def comp_perimeter(self):
        for x in self:
            x.nbre_perimeter = len(x.perimeters_ids)

    @api.depends('treat_date')
    def comp_duration(self):
        if self.treat_date:
            for x in self:
                now = datetime.now()
                delta = abs((x.treat_date - now).days)
            x.treat_duration = delta

    def action_draft(self):
        for x in self:
            x.state = 'brouillon'

    def action_submissive(self):
        for x in self:
            x.state = 'soumise'

    def action_processing(self):
        for x in self:
            x.state = 'entraitement'

    def action_treated(self):
        for x in self:
            x.state = 'traite'
            x.treat_date = datetime.now()

    def action_scheduled(self):
        day = self.env['kzm.instance.request'].search([('limit_date', '<=', date.today() + timedelta(days=5))])
        for x in day:
            x.action_submissive()

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('instance.reconcile') or _('New')
        res = super(Instance_Request, self).create(vals)
        return res

    # def unlink(self):
    #     for state in self:
    #         if state.name != 'brouillon':
    #             raise exceptions.UserError(_("Cannot delete an instance which is in a state different to draft"))
    #         return super().unlink()

    def unlink(self):
        for x in self:
            if x.state != 'brouillon':
                raise ValidationError(_("You can only delete instance requests in Draft status!"))
            return super(Instance_Request, x).unlink()

    def write(self, vals):
        if vals.get('limit_date'):

            users = self.env.ref('kzm_instance_request.group_kzm_instance_request_responsible').users
            for user in users:
                self.activity_schedule('kzm_instance_request.activity_mail_a_traite', user_id=user.id,
                                       note=f' please approve the {self.reference} instance')

            date_time_obj = datetime.strptime(vals['limit_date'], '%Y-%m-%d')
            d = date_time_obj.date()
            if d < date.today():
                raise ValidationError(_("You cannot set a deadline later than today!!"))
        return super(Instance_Request, self).write(vals)
