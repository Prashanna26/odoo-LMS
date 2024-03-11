from odoo import fields, models, api,_
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class LmsDashboard(models.Model):
    _name = 'lms.dashboard'
    _description = "Library Management System - Dashbaord"

    name = fields.Char()
    is_books_card = fields.Boolean(default=False)
    is_sales_card = fields.Boolean(default=False)
    is_borrow_card = fields.Boolean(default=False)
    books_total = fields.Integer(compute="_compute_books_total")
    sold_total = fields.Integer(compute="_compute_books_total")
    borrow_total = fields.Integer(compute="_compute_books_total")
    color = fields.Integer("Color")



    # is_amount_card = fields.Boolean(default=False)
    # total_amount = fields.Integer(compute="_compute_books_total")


    def _compute_books_total(self):
        for dash in self:
            dash.books_total = self.env["lms.books"].search_count([("id", "!=", None)])
            dash.sold_total = self.env["lms.books"].search_count([("state","=","bought")])
            dash.borrow_total = self.env["lms.books"].search_count([("state","=","borrow")])
            # amount = self.env["account.move"].search([("amount_total_signed" , "=" , vals)])
            # dash.total_amount = sum(amount)


