import shared
import test as t
from loguru import logger
#logger.add('test_aoi.log', format='{time} {name} {message}', level='DEBUG', rotation="500 MB", retention="10 days")


polygon = '((-5 40.4, 29 40.4, 29 62, -5 62, -5 40.4))'
server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.quietoceans_v2.value
label = 'aoi test'
test = t.Test(server=server,port=port, token=token, label=label, polygon=polygon, max_lines=1000000)
test.validate_aoi()