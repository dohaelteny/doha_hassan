from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

class HdTicket(models.Model):
    _name = "hd.ticket"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ticket_seq = fields.Char('Ticket ID', default=lambda self: 'New', readonly=True)
    name = fields.Char('Name', help="high-level description of issue", tracking=True)
    checkin_time = fields.Datetime('Time Submitted',readonly=True,default= fields.Datetime.today(), tracking=True,)
    today = fields.Datetime(default=fields.Datetime.today())
    descrption = fields.Html('Description', required=True, tracking=True,)
    team_id = fields.Many2one('hd.team', string='Team', tracking=True,)
    user_id = fields.Many2one('res.users', string='Assigned to', tracking=True, default= lambda self: self.env.user)
    priority = fields.Selection([
        ('low', 'Low'),('medium','Medium'),('high','High'),
    ], string='Priority', tracking=True,)
    customer_id = fields.Many2one('res.partner', string='Customer',required=True, tracking=True,)
    customer_name = fields.Char(related='customer_id.name', string='Customer name', tracking=True,)
    customer_email = fields.Char(related='customer_id.email', string='Customer email', tracking=True,)
    customer_phone = fields.Char(related='customer_id.phone', string='Customer phone', tracking=True,)
    tags = fields.Many2one('crm.tag', string="Tags")
    hosting_type = fields.Selection([
        ('on-premise', 'On-premise'),('cloud','Cloud')
    ], string='Hosting type',required=True, tracking=True,)
    # server_url = fields.
    resolution_time = fields.Integer('Resolution time', compute="calculate_resolution_time")
    state = fields.Selection([
        ('new', 'New'),('in_progress','In Progress'),('solved','Solved'),('cancelled','Cancelled'),
    ], default='new', string='Status')

    @api.depends('checkin_time')
    def calculate_resolution_time(self):
        self.resolution_time = 0
        if self.checkin_time and self.today:
            day1 = datetime.strptime(str(self.checkin_time),'%Y-%m-%d %S:%M:%H')
            print('____________day1',day1)
            day2 = datetime.strptime(str(fields.Datetime.today()),'%Y-%m-%d %S:%M:%H')
            day3 = day2-day1
            self.resolution_time=str(day3.days)

    @api.model
    def create(self, vals):
        if vals.get('ticket_seq', 'NEW') == 'NEW':
            vals['ticket_seq'] = self.env['ir.sequence'].next_by_code('hd.ticket') or 'NEW'
        result = super(HdTicket, self).create(vals)
        return result

    def action_progress(self):
        self.state = 'in_progress'

    def action_solve(self):
        self.state = 'solved'

    def action_cancel(self):
        self.state = 'cancelled'

    def unlink(self):
        for rec in self:
            if rec.state in ['in_progress','solved']:
                raise ValidationError(_('Sorry, you cannot delete the ticket.'))

class CrmTags(models.Model):
    _inherit = "crm.tag"

    ticket_id = fields.Many2one('hd.ticket')

class HelpPartner(models.Model):
    _inherit = "res.partner"

    
    count_ticket = fields.Float('Count Tickets', compute="compute_count")

    def compute_count(self):
        for record in self:
            record.count_ticket = self.env['hd.ticket'].search_count(
                [('customer_id', '=', self.id)])

    def get_tickets(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tickets',
            'view_mode': 'tree',
            'res_model': 'hd.ticket',
            'domain': [('customer_id', '=', self.id)],
            'context': "{'create': False}",
        }

class HelpUser(models.Model):
    _inherit = "res.users"

    count_ticket = fields.Float('Count Tickets', compute="compute_count")

    def compute_count(self):
        for record in self:
            record.count_ticket = self.env['hd.ticket'].search_count(
                [('user_id', '=', self.id)])

    def get_tickets(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tickets',
            'view_mode': 'tree',
            'res_model': 'hd.ticket',
            'domain': [('user_id', '=', self.id)],
            'context': "{'create': False}",
        }