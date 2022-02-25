import shared
import test as t
from loguru import logger
logger.add('logs/test.validate_no_dynamic_down_feed_no_dynamic.log', format='{time} {name} {message}', level='DEBUG',
           retention="1 days")

server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.down_v2_sat_terrestrial.value

label = 'sat_plus_terrestrial'
test = t.Test(server=server, port=port, token=token, max_lines=100000, label=label)
test.validate_no_dynamic()
logger.info("TEST COMPLETED")