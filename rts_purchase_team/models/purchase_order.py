from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_team_id = fields.Many2one('purchase.team', string='Purchase Team')

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-assign first purchase team when creating PO"""
        for vals in vals_list:
            # If no team is specified, auto-assign the first team the user belongs to
            if not vals.get('purchase_team_id'):
                user_id = vals.get('user_id', self.env.user.id)
                team = self.env['purchase.team'].search([
                    '|',
                    ('user_ids', 'in', [user_id]),
                    ('team_leader_id', '=', user_id)
                ], limit=1, order='id asc')

                if team:
                    vals['purchase_team_id'] = team.id

        return super().create(vals_list)

    @api.onchange('user_id')
    def _onchange_user_id(self):
        """Update team when user changes"""
        if self.user_id and not self.purchase_team_id:
            team = self.env['purchase.team'].search([
                '|',
                ('user_ids', 'in', [self.user_id.id]),
                ('team_leader_id', '=', self.user_id.id)
            ], limit=1, order='id asc')

            if team:
                self.purchase_team_id = team.id