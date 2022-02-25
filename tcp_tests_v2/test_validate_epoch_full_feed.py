import shared
import test as t
from loguru import logger
logger.add('logs/test.validate_epoch.log', format='{time} {name} {message}', level='DEBUG',
           retention="1 days")

server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.full_v2.value

label = 'full_feed'
test = t.Test(server=server, port=port, token=token, max_lines=100000, label=label)
test.validate_epoch()
logger.info("TEST COMPLETED")
