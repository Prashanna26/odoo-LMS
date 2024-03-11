from odoo import fields, models, api,_
from datetime import datetime
from odoo.exceptions import ValidationError

class LmsMember(models.Model):
    _name = 'lms.member'
    _description = "Library Management System - Members"

    name = fields.Char('Name', required=True)
    image = fields.Binary(string='Image')
    email = fields.Char('Email')
    address = fields.Char(string='Address')
    dob = fields.Date(string="Date of Birth") 
    phone = fields.Char('Phone Number' ,size=10)
    country = fields.Char(string="Country")
    city = fields.Char()
    membership_type = fields.Selection([
        ('regular','Regular'),
        ('student','Student'),
        ('senior','Senior Citizen'),
        ('temporary','Temporary')
        ], string="Membership Type", default='Regular')
    
    books_ids = fields.Many2many('lms.books', compute="_compute_book_ids")
    history_ids = fields.One2many("lms.history","member_id")
    
    def _compute_book_ids(self):
        for buyer in self:
            buyer.books_ids = self.env["lms.books"].search([("buyer_id","=",buyer.id),("state","=",'borrow')]).ids

    def return_action_to_open_history(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window']._for_xml_id(xml_id)
            res.update(
                context=dict(self.env.context, default_member_id=self.id, group_by=False),
                domain=[('member_id', '=', self.id)]
            )
            return res
        return False  
