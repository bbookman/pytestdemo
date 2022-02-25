import shared
import test as t
from loguru import logger
logger.add('logs/test.validate_no_terrestrial_full_feed_no_terrestrial.log', format='{time} {name} {message}', level='DEBUG',
           retention="1 days")

server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.full_v2_no_terrestrial.value

label = 'full_no_terrestrial'
test = t.Test(server=server, port=port, token=token, max_lines=100000, label=label)
test.validate_no_terrestrial()
logger.info("TEST COMPLETED")