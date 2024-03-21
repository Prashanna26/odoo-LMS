from odoo import fields, models, api

class  LmsOffer(models.Model):
    _name = 'lms.offer'
    _description = "Library Management System - Offers"

    name = fields.Char(string='Title', required=True)
    offer_value = fields.Integer(string='Value', required=True)