# -*- coding: utf-8 -*-
from odoo import http

# class EditableCurrency(http.Controller):
#     @http.route('/editable_currency/editable_currency/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/editable_currency/editable_currency/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('editable_currency.listing', {
#             'root': '/editable_currency/editable_currency',
#             'objects': http.request.env['editable_currency.editable_currency'].search([]),
#         })

#     @http.route('/editable_currency/editable_currency/objects/<model("editable_currency.editable_currency"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('editable_currency.object', {
#             'object': obj
#         })