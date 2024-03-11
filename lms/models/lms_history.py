from odoo import fields, models, api,_
from odoo.exceptions import UserError

class LmsHistory(models.Model):
    _name = 'lms.history'
    _description = "Library Management System - History"

    name = fields.Char(compute="_compute_name")
    person_name = fields.Char()
    start_date = fields.Date()
    end_date = fields.Date()
    state = fields.Selection([('0', 'Not Yet'), ('1','Lent Out')], string="Status")
    books_id = fields.Many2one('lms.books')
    member_id = fields.Many2one('lms.member')


    def _compute_name(self):
        for his in self:
            his.name = his.books_id.name + '-' + his.member_id.name