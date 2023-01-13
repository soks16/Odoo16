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
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    ref = fields.Char(string="Reference")
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High')],
        string='Priority', tracking=True)


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        for x in self:
            x.ref = x.patient_id.ref
