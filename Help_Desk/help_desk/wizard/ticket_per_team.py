from odoo import fields, api, models, _ 

class TicketPerTeamWizard(models.TransientModel):
    _name = "ticket.per.team.wizard"

    team_id  = fields.Many2one('hd.team', string='Team')

    state = fields.Selection([
        ('new', 'New'),('in_progress','In Progress'),('solved','Solved'),('cancelled','Cancelled'),
    ], default='new', string='Status')

    def print_pdf(self):
        tickets_state = self.env['hd.ticket'].search([('team_id','=',self.team_id.id),('state','=',self.state)])
        tickets_without_state = self.env['hd.ticket'].search([('team_id','=',self.team_id.id)])
        
        if self.state:
            data = {
                # 'ids':[],
                # 'model': 'ticket.per.team.wizard',
                'tickets': tickets_state,  
            }
            print('_____________________data',data)
        else:
            data = {
                # 'ids':[],
                # 'model': 'ticket.per.team.wizard',
                'tickets_without_state': tickets_without_state,
            }
            print('_++++++++++++++++++++++++data',data)
        return self.env.ref('help_desk.tickets_per_team_action').report_action(self, data=data)
  