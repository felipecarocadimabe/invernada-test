# -*- coding: utf-8 -*-
from odoo import http

# class OpenfacturaIntegration(http.Controller):
#     @http.route('/openfactura_integration/openfactura_integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openfactura_integration/openfactura_integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openfactura_integration.listing', {
#             'root': '/openfactura_integration/openfactura_integration',
#             'objects': http.request.env['openfactura_integration.openfactura_integration'].search([]),
#         })

#     @http.route('/openfactura_integration/openfactura_integration/objects/<model("openfactura_integration.openfactura_integration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openfactura_integration.object', {
#             'object': obj
#         })