from handlers.main import Main
from handlers.reduce import Reduce
from handlers.reduce_local_handler import ReduceLocal
from handlers.status import Status
from handlers.table import Table
from handlers.table2 import Table2
from handlers.table3 import Table3

routes = [
    ('GET', '/', Main, 'main'),
    ('GET', '/status', Status, 'status'),
    ('POST', '/table', Table3, 'table'),
    ('GET', '/table2', Table2, 'table2'),
    ('POST', '/reduce', ReduceLocal, 'reduce'),
]
