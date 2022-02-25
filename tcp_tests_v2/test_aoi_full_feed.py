import shared
import test as t
from loguru import logger
logger.add('logs/test_validate_aoi_full_feed_w_aoi.log', format='{time} {name} {message}', level='DEBUG',
           retention="1 days")


server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.quietoceans_v2.value

label = 'full_feed_w_aoi'
test = t.Test(server=server, port=port, token=token, max_lines=1000000, label=label)
test.validate_aoi()
logger.info("TEST COMPLETED")
