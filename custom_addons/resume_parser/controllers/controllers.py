# -*- coding: utf-8 -*-
# from odoo import http


# class ResumeParser(http.Controller):
#     @http.route('/resume_parser/resume_parser/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/resume_parser/resume_parser/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('resume_parser.listing', {
#             'root': '/resume_parser/resume_parser',
#             'objects': http.request.env['resume_parser.resume_parser'].search([]),
#         })

#     @http.route('/resume_parser/resume_parser/objects/<model("resume_parser.resume_parser"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('resume_parser.object', {
#             'object': obj
#         })
