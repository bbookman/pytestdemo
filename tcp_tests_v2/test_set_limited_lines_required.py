import shared
import test as t
from loguru import logger
logger.add('test_set_limited_lines_required.log', format='{time} {name} {message}', level='DEBUG',
           retention="10 days")

total_tests = 17
logger.info(f"TOTAL TESTS TO EXECUTE: {total_tests}")

# FULL TOKEN, NO FILTERS
server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.full_v2.value

# full v2
label = 'full_feed'
test_number = ''

test = t.Test(server=server, port=port, token=token, max_lines=100000, label=label)

test_number = 1
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""

logger.info(details)
test.validate_terrestrial()
test_number = 2
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_ais_required_fields()
test_number = 3
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_epoch()
test_number = 4
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
test.validate_norad_id()
test = t.Test(server=server, port=port, token=token, max_lines=100000000, label=label)
test_number = 5
logger.info(details)
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
test.validate_dynamic()
test_number = 6
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_message_types()

label = 'just_sat'
test = t.Test(server=server, port=port, token=shared.Tokens.down_v2_sat_only_no_norad.value, max_lines=100000, label=label)
test_number = 7
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_spire_id()

# full no g tags
label = 'full_no_g_tag'
token = shared.Endpoints.full_v2_no_g_tags.value
test = t.Test(server=server, port=port, token=token, max_lines=100000, label=label)
test_number = 8
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_no_g_tags()

# full no terrestrial
label = 'full_no_terrestrial'
token = shared.Endpoints.full_v2_no_terrestrial.value
test = t.Test(server=server, port=port, token=token, max_lines=100000, label=label)
test_number = 9
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_no_terrestrial()

# down_v2_sat_only_no_norad
label = 'down_no_norad'
token = shared.Endpoints.down_v2_sat_only_no_norad.value
test = t.Test(server=server, port=port, token=token, max_lines=100000, label=label)
test_number = 10
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_no_norad_id()

# full_v2_no_spire
label = 'full_no_spire'
token = shared.Endpoints.full_v2_no_spire.value
test = t.Test(server=server, port=port, token=token, max_lines=100000, label=label)
test_number = 11
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_no_spire_id()

# no dynamic
label = 'down_no_dynamic'
token = shared.Endpoints.down_v2_no_navtor_no_navtor_b.value
test = t.Test(server=server, port=port, token=token, max_lines=100000000, label=label)
test_number = 12
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_no_dynamic()

label = 'sat_plus_terrestrial'
token = shared.Endpoints.down_v2_sat_terrestrial.value
test = t.Test(server=server, port=port, token=token, max_lines=100000000, label=label)
test_number = 13
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_no_dynamic()
test_number = 14
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""

label = 'sat_plus_terrestrial'

logger.info(details)
test.validate_epoch()
test_number = 15
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_spire_id()
test_number = 16
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_terrestrial()

polygon = '((-5 40.4, 29 40.4, 29 62, -5 62, -5 40.4))'
server = shared.Endpoints.v2_production.value
port = shared.Ports.v2_production.value
token = shared.Tokens.quietoceans_v2.value
label = 'aoi test'
test = t.Test(server=server,port=port, token=token, label=label, polygon=polygon, max_lines=1000000)
test_number = 17
details = f"""TEST INFO {label} | test: {test_number} or {total_tests}"""
logger.info(details)
test.validate_aoi()
logger.info(f"DONE TESTING.  TOTAL TESTS: {total_tests}")
