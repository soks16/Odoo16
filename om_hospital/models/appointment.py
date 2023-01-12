# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient")
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    gender = fields.Selection(related='patient_id.gender')
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
