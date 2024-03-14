from odoo import fields, models, api

class  LmsAuthor(models.Model):
    _name = 'lms.author'
    _description = "Library Management System - Author"
    _order = "sequence"

    name = fields.Char()
    sequence = fields.Integer('Sequence')
    phone = fields.Char('Phone Number', size=16)
    email = fields.Char('Email', required=True)
    description = fields.Text()
    books_ids = fields.Many2many('lms.books', compute="_compute_book_ids")

    def _compute_book_ids(self):
        for author in self:
            author.books_ids = self.env["lms.books"].search([("author_ids","=",author.id)]).ids

     



