import shared
import test as t
from loguru import logger
logger.add('~/logs/test_report_down_catch_up_time.log', format='{time} {name} {message}', level='DEBUG', rotation="500 MB",
           retention="10 days")

server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.down_v2.value
reset_to = '2021-04-08T22:13:00.000Z'   # A|T|v5kv3vPShITK9JRjyNbTUis6S9d6pG9o|2021-04-08T20:07:00.000Z
label = 'downsample_catch_up'
test = t.Test(server=server, port=port, token=token, label=label, reset_string=reset_to)
test.measure_catch_up_time()