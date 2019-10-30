# -*- coding: utf-8 -*-
from odoo import http

# class Openfactura-integration(http.Controller):
#     @http.route('/openfactura-integration/openfactura-integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openfactura-integration/openfactura-integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openfactura-integration.listing', {
#             'root': '/openfactura-integration/openfactura-integration',
#             'objects': http.request.env['openfactura-integration.openfactura-integration'].search([]),
#         })

#     @http.route('/openfactura-integration/openfactura-integration/objects/<model("openfactura-integration.openfactura-integration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openfactura-integration.object', {
#             'object': obj
#         })