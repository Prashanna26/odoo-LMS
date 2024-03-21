from odoo import fields, models, api,_
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class LmsBooks(models.Model):
    _name = 'lms.books'
    _description = "Library Management System - Books"
    _order = "priority desc, name"
    
    name = fields.Char(string=u'Title', required=True)
    description = fields. Text()   
    image = fields.Binary(string='Image')
    author_ids = fields.Many2many('lms.author','books_ids',string='Author')
    edition = fields.Integer(string="Edition")
    isbn = fields.Integer(string="ISBN", unique=True)
    year = fields.Date(string="Published Date")
    published_year = fields.Char(string="Published Year", compute='_compute_published_year', store=True)
    category_ids = fields.Many2many('lms.category')
    state = fields.Selection([
                            ('available','Available'),
                            ('borrow','Borrowed'),
                            ('bought','Bought')],
                            string='Status', default='available')
    price = fields.Integer(string='Price(Rs.)')
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    member_id = fields.Many2one('lms.member', string="Member")
    seller_id = fields.Many2one('res.users', string="seller")
    offer_id = fields.Many2one('lms.offer', string="Offers")
    days_borrow = fields.Integer(default=7, string="Days to Borrow")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorite'),
    ], default='0', string="Favorite")
    history_ids = fields.One2many("lms.history","books_id")
    active = fields.Boolean(default=True)

    @api.depends('year')
    def _compute_published_year(self):
        for record in self:
            if record.year:
                record.published_year = record.year.year
            else:
                record.published_year = ''

    def borrow_action(self):
        for book in self:
            book.seller_id = self.env.user.id
            if book.member_id and book.seller_id:
                book.state = 'borrow'
                present_date = datetime.now()
                history = self.env['lms.history'].create(
                {
                    'books_id': book.id,
                    'member_id':book.member_id.id,
                    'person_name': book.member_id.name,
                    'start_date': present_date,
                    'end_date': present_date + timedelta(days=book.days_borrow),
                    'state': "1"
                })
            elif not book.buyer_id:
                raise UserError(_("Please select a member to whom you want to lend this book."))
                

    def bought_action(self):
        for book in self:
            book.seller_id = self.env.user.id
            if book.buyer_id:
                book.state = 'bought'
            elif not book.buyer_id:
                raise UserError(_("Please select a Buyer to whom you want to buy this book."))
                

    def available_action(self):
        present_date = datetime.now()
        for book in self:
            if book.state == 'borrow':
                book.history_ids.end_date = present_date
                book.history_ids.state = '0'
            book.state = 'available'
            book.buyer_id = ''
            book.seller_id = ''
            book.days_borrow = 7

    def return_action_to_open_history(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window']._for_xml_id(xml_id)
            res.update(
                context=dict(self.env.context, default_books_id=self.id, group_by=False),
                domain=[('books_id', '=', self.id)]
            )
            return res
        return False    



    
    