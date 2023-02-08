# -*- coding: utf-8 -*-
# from odoo import http


# class LocationApp(http.Controller):
#     @http.route('/location_app/location_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/location_app/location_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('location_app.listing', {
#             'root': '/location_app/location_app',
#             'objects': http.request.env['location_app.location_app'].search([]),
#         })

#     @http.route('/location_app/location_app/objects/<model("location_app.location_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('location_app.object', {
#             'object': obj
#         })
