{
    'name': 'Multiuser To-Do',
    'description': 'Extend To-Do Tasks for multiuser',
    'author': 'Luis Andia',
    'depends': ['todoapp', 'mail'],
    'data': ['views/todo_task.xml', 'security/todo_access_rules.xml'],
    'demo': [
            # Ch04 Data files
        'data/todo.task.csv',
        'data/todo_data.xml',
    ],
}
