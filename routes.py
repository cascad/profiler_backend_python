from handlers.main import Main
from handlers.status import Status
from handlers.table import Table
from handlers.table2 import Table2

routes = [
    ('GET', '/', Main, 'main'),
    ('GET', '/status', Status, 'status'),
    ('POST', '/table', Table, 'table'),
    ('GET', '/table2', Table2, 'table2'),
]
