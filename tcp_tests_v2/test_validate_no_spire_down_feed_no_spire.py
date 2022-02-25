import shared
import test as t
from loguru import logger
logger.add('logs/test.validate_no_spire_down_feed_no_spire.log', format='{time} {name} {message}', level='DEBUG',
           retention="1 days")

server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.down_v2_no_spire

label = 'down_feed_no_spire'
test = t.Test(server=server, port=port, token=token, max_lines=1000000, label=label)
test.validate_no_spire_id()
logger.info("TEST COMPLETED")
