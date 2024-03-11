from odoo import _, models

# Estate Property Model
class LmsBooks(models.Model):
    _inherit = "lms.books"
    
    def bought_action(self):
        res = super(LmsBooks, self).bought_action()
        for books in self:
            selling_price = books.price
            invoice = self.env['account.move'].create(
                {
                'partner_id': books.buyer_id.id, 
                'move_type': 'out_invoice',
                'invoice_line_ids':[
                    (0, 0, {
                    'name': books.name,
                    'quantity': 1,
                    'price_unit': selling_price,
                })
                ]
            })
        return res
    