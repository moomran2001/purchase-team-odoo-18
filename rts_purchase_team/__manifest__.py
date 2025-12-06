{
    'name': 'Purchase Teams',
    'version': '18.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Manage Purchase Teams like Sales Teams',
    'description': """
        Purchase Teams Management
        =========================
        This module adds Purchase Teams functionality similar to Sales Teams:
        * Create and manage purchase teams
        * Assign team leaders
        * Link purchase orders to teams
        * Configuration menu for purchase teams
    """,
    'author': 'Rightechs Solutions',
    'website': 'https://www.rightechs.net',
    'depends': ['purchase', 'base', 'mail'],
    'data': [
        'security/purchase_team_security.xml',  # أضف هنا
        'security/ir.model.access.csv',
        # 'views/menus.xml',
        'views/purchase_team_views.xml',
        'views/purchase_order_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}