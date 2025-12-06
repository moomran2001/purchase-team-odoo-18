from odoo import models, fields, api


class PurchaseTeam(models.Model):
    _name = 'purchase.team'
    _description = 'Purchase Team'
    _rec_name = 'name'

    name = fields.Char(string='Team Name', required=True)
    team_leader_id = fields.Many2one('res.users', string='Team Leader', domain=[('share', '=', False)])
    user_ids = fields.Many2many('res.users', 'purchase_team_users_rel', 'team_id', 'user_id',
                                string='Team Members', domain=[('share', '=', False)])
    member_count = fields.Integer(string='Members Count', compute='_compute_member_count')
    purchase_order_count = fields.Integer(string='Purchase Orders', compute='_compute_purchase_order_count')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    purchase_order_ids = fields.One2many('purchase.order', 'purchase_team_id', string='Purchase Orders')

    @api.depends('user_ids')
    def _compute_member_count(self):
        for team in self:
            team.member_count = len(team.user_ids)

    @api.depends('purchase_order_ids')
    def _compute_purchase_order_count(self):
        for team in self:
            team.purchase_order_count = len(team.purchase_order_ids)

    def action_view_members(self):
        """Open a window to view team members"""
        return {
            'name': f'{self.name} - Members',
            'view_type': 'form',
            'view_mode': 'kanban,list,form',
            'res_model': 'res.users',
            'domain': [('id', 'in', self.user_ids.ids)],
            'type': 'ir.actions.act_window',
        }

    def action_view_purchase_orders(self):
        """Open a window to view team's purchase orders"""
        return {
            'name': f'{self.name} - Purchase Orders',
            'view_type': 'form',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'domain': [('purchase_team_id', '=', self.id)],
            'type': 'ir.actions.act_window',
        }

    def action_add_members(self):
        """Open wizard to add team members"""
        return {
            'name': 'Add: Team Members',
            'type': 'ir.actions.act_window',
            'res_model': 'add.purchase.team.members',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_team_id': self.id,
            },
        }