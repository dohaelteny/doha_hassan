from odoo import fields, api, models, _ 


# class Usersheolp(models.Model):
#     _inherit = "res.users"

#     team_id  = fields.Many2one('hd.team', string='Team')

class HdTeam(models.Model):
    _name = "hd.team"

    name = fields.Char('Name')
    team_manager  = fields.Many2one('hd.team', string='Team Manager')
    # member_ids = fields.One2many('res.users', 'team_id', string='Member')

