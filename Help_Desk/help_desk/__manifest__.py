{
    'name' : 'Help Desk',
    'version' : '14',
    'summary': 'Ticketing Help Desk ',
    'depends':['base','mail','crm','account'],
    'data':[
        'security/help_desk_group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/ticket_per_team_pdf.xml',
        'wizard/ticket_wizard_view.xml',
        'views/hd_team.xml',
        'views/hd_ticket.xml',
        'views/cutomer_view.xml',
        'views/users_view.xml',
    ],

    
}