# -*- coding: utf-8 -*-
from odoo import http

# class FollowPurchase(http.Controller):
#     @http.route('/follow_purchase/follow_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/follow_purchase/follow_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('follow_purchase.listing', {
#             'root': '/follow_purchase/follow_purchase',
#             'objects': http.request.env['follow_purchase.follow_purchase'].search([]),
#         })

#     @http.route('/follow_purchase/follow_purchase/objects/<model("follow_purchase.follow_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('follow_purchase.object', {
#             'object': obj
#         })