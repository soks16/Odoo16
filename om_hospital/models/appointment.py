# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'ref'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient")
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    gender = fields.Selection(related='patient_id.gender')
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today, help="Booking date")
    ref = fields.Char(string="Reference", help="Reference from patient record")
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High')],
        string='Priority', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        string='Status', tracking=True, default='draft')

    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)

    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string="Hide Sales Price")

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        for x in self:
            x.ref = x.patient_id.ref

    def action_test(self):
        print("Button clicked")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successfull',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for i in self:
            i.state = 'in_consultation'

    def action_done(self):
        for i in self:
            i.state = 'done'

    def action_cancel(self):
        for i in self:
            i.state = 'cancel'

    def action_draft(self):
        for i in self:
            i.state = 'draft'


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string='Price', related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default="1")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
