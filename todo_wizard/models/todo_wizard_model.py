from odoo import models, fields, api
from odoo import exceptions

import logging
_logger = logging.getLogger(__name__)


class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    _description = 'To-do Mass Assignment'
    task_ids = fields.Many2many('todo.task', string='Tasks')
    new_deadline = fields.Date('Set Deadline')
    new_user_id = fields.Many2one('res.users', string='Set Responsible')




