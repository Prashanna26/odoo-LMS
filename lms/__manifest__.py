{
    'name': 'lms',
    'author':'Prashanna',
    'sequence': -1,
    'website': 'https://www.lms.tech',
    'summary': 'Library Management System development',
    'depends': ['base', 'account'],
    'data': [
        #  security
        'security/ir.model.access.csv',

        # data
        'data/dashboard_data.xml',
        
        # views
        'views/lms_dashboard_view.xml',
        'views/lms_book_view.xml',
        'views/lms_author_view.xml',
        'views/lms_category_view.xml',
        'views/lms_member_view.xml',
        'views/lms_history_view.xml',
        'views/lms_dashboard_view.xml',
        'views/lms_offer_view.xml',
    ],
    'assets': {},
    'demo':[],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}