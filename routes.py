from handlers.main import Main
from handlers.status import Status
from handlers.table import Table
from handlers.table2 import Table2

routes = [
    ('GET', '/analytics/', Main, 'main'),
    ('GET', '/analytics/status', Status, 'status'),
    ('GET', '/analytics/table', Table, 'table'),
    ('GET', '/analytics/table2', Table2, 'table2'),
]
