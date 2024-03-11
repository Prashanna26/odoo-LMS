from odoo import fields, models, api

class  LmsCategory(models.Model):
    _name = 'lms.category'
    _description = "Library Management System - Category"

    name = fields.Char()
    color = fields.Integer("Color")