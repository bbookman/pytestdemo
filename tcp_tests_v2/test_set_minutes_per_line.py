import test as t
import shared
from loguru import logger
logger.add('test_minutes_per_line.log', format='{time} {name} {message}', level='DEBUG', rotation="500 MB",
           retention="10 days")

"""
token: CHANGE THE TOKEN BELOW DEPENDING ON TEST DESIRED
max_lines: the number of lines to run
"""
token = shared.Tokens.down_v2_sat_only_no_norad.value
max_lines = 100000000
server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
test = t.Test(server=server, port=port, token=token, max_lines=max_lines)
test.minutes_per_line()