import shared
import test as t
from loguru import logger
#logger.add('test_save_local.log', format='{time} {name} {message}', level='DEBUG', rotation="500 MB",retention="10 days")

server = shared.Endpoints.v1_production.value
port = shared.Ports.v1_production.value
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lciI6eyJpZCI6IjkwNCIsIm5hbWUiOiJTQUlTT05MWUJSVUNFIiwidXVpZCI6IjkwNCJ9LCJpc3MiOiJzcGlyZS5jb20iLCJpYXQiOjE2MTcxNjA3MjZ9.OwG5quvT8niy9FYpaw3HW_0sT0DN8Kdl2fPnCxouz1g"

test = t.Test(server=server, port=port, token=token, max_lines=10000)
test.save_data_local()