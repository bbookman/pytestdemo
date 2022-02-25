import src.constants as constants
import src.utilities as utilities
import pytest
from nested_lookup import nested_lookup as nl


#   PURPOSE confirm tokens with limits are really limited
#   A:  limit by imo returns only expected imo
#   B:  limit by mmsi returns only expected mmsi
#   C:  limit by shipType returns only expected shipType
#   D:  limit by AOI returns only positions within AOI
#
#   Positive product tests
#   E:  allow Maritime Port Matching Graphql
#   F:  allow Maritime Geo Routing Graphql
#   G:  allow Maritime Vessels Graphql
#   H:  allow Maritime Extended Vessel Characteristics Graphql
#   Negative product tests
#   I:  if Port Matching, deny Vessels, Geo routing , extended char
#   J:  if Geo routing, deny Vessels, port, extended
#   K:  if Vessels, deny Port, Geo routing and extended
#   L:  if Extended, deny Port and Geo routing
#   M:  if Basic, deny extended, port, geo routing


# Apigee record
# https://apigee.com/organizations/spire/apps/details/833236a1-ac21-4aff-91a7-b46c93414d7a
# 9513842, 9426776, 8510221, 9490741, 9639830
@pytest.mark.parametrize('token_id, expected_imo_list',
                         [('IMO_RESTRICTED_B',
                           [9513842, 9426776, 8510221, 9490741, 9639830])],
                         ids=str)
def test_limited_imo(token_id, expected_imo_list, url, timeout, retries):
    #  ARRANGE
    client = utilities.generate_client(url=url,
                                       timeout=timeout,
                                       retries=retries,
                                       token_id=token_id)
    query: str = utilities.build_vessel_query(segments=[constants.static_data_segment])

    #   ACT
    response, err = utilities.get_single_page_response(connection=client,
                                                       query=query)
    response_imo: list = nl('imo', response)
    #   ASSERT
    assert set(expected_imo_list) == set(response_imo), query


#  Apigee record
# https://apigee.com/organizations/spire/apps/details/baa88302-d99f-49d1-9d5f-c3b78d005027
# 210350000,477698600,257275000
@pytest.mark.parametrize('token_id, expected_mmsi_list',
                         [('MMSI_RESTRICTED_A',
                           [210350000, 477698600, 257275000])],
                         ids=str)
def test_limited_mmsi(token_id, expected_mmsi_list, url, timeout, retries):
    #  ARRANGE
    client = utilities.generate_client(url=url,
                                       timeout=timeout,
                                       retries=retries,
                                       token_id=token_id)
    query: str = utilities.build_vessel_query(segments=[constants.static_data_segment])

    #   ACT
    response, err = utilities.get_single_page_response(connection=client,
                                                       query=query)
    #   ASSERT
    response_mmsi: list = nl('mmsi', response)
    assert set(expected_mmsi_list) == set(response_mmsi), query


#   C:  limit by shipType returns only expected shipType
# https://apigee.com/organizations/spire/apps/details/b65253e7-8a10-456f-ae65-e9d4708d9fa0
# TANKER_CRUDE, CONTAINER, FISHING
@pytest.mark.parametrize('token_id, expected_ship_types',
                         [('SHIP_TYPE_RESTICTED_A', ['TANKER_CRUDE', 'CONTAINER', 'FISHING'])],
                         ids=str)
def test_limited_ship_types(token_id,
                            expected_ship_types,
                            url,
                            retries,
                            timeout):
    #  ARRANGE
    client = utilities.generate_client(url=url,
                                       timeout=timeout,
                                       retries=retries,
                                       token_id=token_id)
    query: str = utilities.build_vessel_query(segments=[constants.static_data_segment])
    #   ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='shipType',
                                             limit=10)
    response_ship_types: set = set()
    for ship_type in responses:
        response_ship_types.add(ship_type)
    #   ASSERT
    assert set(expected_ship_types) == response_ship_types, query


#   D:  limit by AOI returns only positions within AOI
# https://apigee.com/organizations/spire/apps/details/4f8c4a12-3ff3-4754-8f91-444f677e857d
@pytest.mark.parametrize('token_id, polygon',
                         [('AOI_A', constants.aoi_a_for_token_limit_test)],
                         ids=str)
def test_limited_by_aoi(token_id,
                        polygon,
                        url,
                        retries,
                        timeout):
    #  ARRANGE
    client = utilities.generate_client(url=url,
                                       timeout=timeout,
                                       retries=retries,
                                       token_id=token_id)
    query: str = utilities.build_vessel_query(segments=[constants.last_position_update_segment])

    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='lastPositionUpdate',
                                             limit=10)
    polygon = utilities.make_polygon(polygon)
    for response in responses:
        #  Each response is a list w/ lat[0] and long[1]
        latitude: float = response[0]
        longitude: float = response[1]
        point = utilities.make_point(latitude=latitude, longitude=longitude)
        assert utilities.point_is_within_aoi(point=point, polygon=polygon), query


#   Positive product tests
#   E:  allow Maritime Port Matching Graphql
#   F:  allow Maritime Geo Routing Graphql
#   G:  allow Maritime Vessels Graphql
#   H:  allow Maritime Extended Vessel Characteristics Graphql
@pytest.mark.parametrize('token_id, prod_to_allow',
                         [('PORT_ONLY',
                           'port'),
                          ('ROUTE_ONLY_B',
                           'route'),
                          ('VESSELS_ONLY',
                           'vessels'),
                          ('VESSEL_CHAR_EXTENDED',
                           'extended'),
                          ('VESSEL_CHAR_BASIC',
                           'basic')
                          ],
                         ids=str
                         )
def test_product_positive(token_id,
                          prod_to_allow,
                          url,
                          timeout,
                          retries):
    #  ARRANGE
    client = utilities.generate_client(url=url,
                                       timeout=timeout,
                                       retries=retries,
                                       token_id=token_id)

    if prod_to_allow == 'port':
        query: str = utilities.build_port_query(unlocode='USNYC')
    elif prod_to_allow == 'route':
        query: str = utilities.build_predicted_vessel_route_query(destination_unlocode="USNYC",
                                                                  origin_unlocode='AERUW',
                                                                  imo=9534793)
    elif prod_to_allow == 'extended':
        query: str = utilities.build_vessel_query(segments=[constants.static_data_segment,
                                                            constants.characteristics_extended_segment])
    elif prod_to_allow == 'basic':
        query: str = utilities.build_vessel_query(segments=[constants.static_data_segment,
                                                            constants.characteristics_basic_segment])
    elif prod_to_allow == 'vessels':
        query: str = utilities.build_vessel_query(segments=[constants.static_data_segment])

    #  ACT
    data, err = utilities.get_single_page_response(connection=client, query=query)

    #  ASSERT
    #  some data shows up someplace
    got_data: bool = False
    for k, v in data.items():
        if v:
            got_data = True
    assert got_data, query



#   Negative product tests
#   I:  if Port Matching, deny Vessels, Geo routing , extended char
#   J:  if Geo routing, deny Vessels, port, extended
#   K:  if Vessels, deny Port, Geo routing and extended
#   L:  if Extended, deny Port and Geo routing
#   M:  if Basic, deny extended, port, geo routing

@pytest.mark.parametrize('token_id, expected_error, prod_to_deny',
                         [('PORT_ONLY',
                           constants.expected_bad_token_response,
                           'vessels'),
                          ('PORT_ONLY',
                           constants.expected_bad_token_response,
                           'extended'),
                          ('PORT_ONLY',
                           constants.expected_bad_token_response,
                           'routing'),
                          ('ROUTE_ONLY_B',
                           constants.expected_bad_token_response,
                           'extended'),
                          ('ROUTE_ONLY_B',
                           constants.expected_bad_token_response,
                           'vessels'),
                          ('ROUTE_ONLY_B',
                           constants.expected_bad_token_response,
                           'port'),
                          ('VESSELS_ONLY',
                           constants.expected_bad_token_response,
                           'port'
                           ),
                          ('VESSELS_ONLY',
                           constants.expected_bad_token_response,
                           'extended'
                           ),
                          ('VESSELS_ONLY',
                           constants.expected_bad_token_response,
                           'routing'
                           ),
                          ('VESSEL_CHAR_EXTENDED',
                           constants.expected_bad_token_response,
                           'routing'
                           ),
                          ('VESSEL_CHAR_EXTENDED',
                           constants.expected_bad_token_response,
                           'port'
                           ),
                          ('VESSEL_CHAR_BASIC',
                           constants.expected_bad_token_response,
                           'extended'
                           ),
                          ('VESSEL_CHAR_BASIC',
                           constants.expected_bad_token_response,
                           'port'
                           ),
                          ('VESSEL_CHAR_BASIC',
                           constants.expected_bad_token_response,
                           'routing'
                           )
                          ],
                         ids=str)
def test_product_negative(token_id,
                          expected_error,
                          url,
                          retries,
                          timeout,
                          prod_to_deny):
    #  ARRANGE
    client = utilities.generate_client(url=url,
                                       timeout=timeout,
                                       retries=retries,
                                       token_id=token_id)
    if prod_to_deny == 'vessels':

        query: str = utilities.build_vessel_query(segments=[constants.static_data_segment])
    elif prod_to_deny == 'extended':
        query: str = utilities.build_vessel_query(segments=[constants.static_data_segment,
                                                            constants.characteristics_extended_segment])
    elif prod_to_deny == 'routing':
        # need a lot of variables, just picking ones - the values really do not matter

        query: str = utilities.build_predicted_vessel_route_query(destination_unlocode="USNYC",
                                                                  origin_unlocode="USNYC",
                                                                  imo=1234567)
    elif prod_to_deny == 'port':
        query: str = utilities.build_port_query('USNYC')

    #  ACT
    data, err = utilities.get_single_page_response(connection=client, query=query)
    #  ASSERT
    assert expected_error in err, f'ALLOWED: {prod_to_deny} for {token_id}'
