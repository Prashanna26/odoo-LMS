from odoo import fields, models, api,_
from datetime import datetime
from  dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class LmsMember(models.Model):
    _name = 'lms.member'
    _description = "Library Management System - Members"

    name = fields.Char('Name', required=True)
    image = fields.Binary(string='Image')
    email = fields.Char('Email')
    address = fields.Char(string='Address')
    dob = fields.Date(string="Date of Birth", default=fields.Date.subtract(fields.Date.today(),years=18)) 
    phone = fields.Char('Phone Number' ,size=10)
    country = fields.Char(string="Country")
    city = fields.Char()
    membership_type = fields.Selection(
        [
        ('regular','Regular'),
        ('student','Student'),
        ('senior','Senior Citizen'),
        ('temporary','Temporary')
        ], string="Membership Type", default='regular')
    mem_cust = fields.Selection(
            [("member","Member"),
            ("customer","Customer+Member")
             ], string='Type', default="member")
    is_customer = fields.Boolean("Customer", default=False)
    
    books_ids = fields.Many2many('lms.books', compute="_compute_book_ids")
    history_ids = fields.One2many("lms.history","member_id")

    def _compute_book_ids(self):
        for buyer in self:
            buyer.books_ids = self.env["lms.books"].search([("member_id","=",buyer.id),("state","=",'borrow')]).ids

    @api.onchange('is_customer')
    def  onchange_mem_cust(self):
        for member in self:
            if member.is_customer == True:
                member.mem_cust = 'customer'

    def customer_action(self):
        for member in self:
            member.is_customer = True       

    @api.constrains('dob')
    def check_date(self):
        for date in self:
            valid_date = datetime.today().date() - relativedelta(years=18)
            if date.dob and (valid_date > date.dob):
                raise ValidationError(_('The member must be at least 18 years old!'))

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
    
    @api.model
    def create(self, vals):
        member = super().create(vals)
        if vals.get('is_customer'):
            self._create_customer(vals)
        return member
    
    def write(self, vals):
        for obj in self:
            if not obj.is_customer:
                partner = self.env['res.partner'].create({
                    'is_company': False,
                    'name': obj.name,
                    'email': obj.email,
                    'phone': obj.phone,
                })
        member = super().write(vals)
        return member

    def _create_customer(self, vals):
        partner_vals = {
            'is_company': False,
            'name': vals.get('name'), 
            'email': vals.get('email'),
            'phone': vals.get('phone'),
        }
        partner = self.env['res.partner'].create(partner_vals)

