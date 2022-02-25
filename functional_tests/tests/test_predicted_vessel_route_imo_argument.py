import pytest
import src.utilities as utilities
from nested_lookup import nested_lookup as nl


#   PURPOSE: Verify providing imo as arg for predicted vessel route returns results
#   - Variables under test include
#       - imo
#       - speed  (a default exists, and will be changed for some tests)
#       - piracy:  defaults to false
#       - canals:  defaults to none
#   NOTE:  veracity of the data is not proven, simply that some response is returned
#
#   POSITIVE:
#   A:  Given imo, data is returned
#   B:  Given imo, speed, data is returned
#   C:  Given imo, piracy = true, data is returned
#   D:  Given imo and canals, data is returned

#   A:  Given imo, data is returned
@pytest.mark.parametrize('imo, origin_unlocode, destination_unlocode',
                         [(9534793, 'DEHAM', 'USNYC')], ids=str)
def test_route_valid_imo_all_other_args_default(client, imo, origin_unlocode, destination_unlocode):
    #  ARRANGE
    query: str = utilities.build_predicted_vessel_route_query(origin_unlocode=origin_unlocode,
                                                              destination_unlocode=destination_unlocode,
                                                              imo=imo)
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    assert response, query
    # Should always get a journey
    journey: dict = nl('journey', response)[0]
    failure_reason: str = ''
    if not journey:
        failure_reason = utilities.get_failure_details(inputs=query,
                                                       expected_outputs='journey not null',
                                                       response=response)
    assert journey, failure_reason


#   B:  Given imo, speed, data is returned
@pytest.mark.parametrize('imo, origin_unlocode, destination_unlocode , speed',
                         [(9772333, 'DEHAM', 'USNYC', 22.2)],
                         ids=str)
def test_route_imo_plus_speed(client,
                              imo,
                              origin_unlocode,
                              destination_unlocode,
                              speed):
    #  ARRANGE
    query: str = utilities.build_predicted_vessel_route_query(origin_unlocode=origin_unlocode,
                                                              destination_unlocode=destination_unlocode,
                                                              imo=imo,
                                                              speed=speed)
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    assert response
    # Should always get a journey
    journey: dict = nl('journey', response)[0]
    failure_reason: str = ''
    if not journey:
        failure_reason = utilities.get_failure_details(inputs=query,
                                                       expected_outputs='journey not null',
                                                       response=response)

    assert journey, failure_reason


#   C:  Given imo, piracy = true, data is returned
@pytest.mark.parametrize('imo, origin_unlocode, destination_unlocode , piracy',
                         [(9772333, 'DEHAM', 'USNYC', 'true')],
                         ids=str)
def test_route_imo_plus_piracy(client,
                               imo,
                               origin_unlocode,
                               destination_unlocode,
                               piracy):
    #  ARRANGE
    query: str = utilities.build_predicted_vessel_route_query(origin_unlocode=origin_unlocode,
                                                              destination_unlocode=destination_unlocode,
                                                              imo=imo,
                                                              piracy=piracy)
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    assert response
    # Should always get a journey
    journey: dict = nl('journey', response)[0]
    failure_reason: str = ''
    if not journey:
        failure_reason = utilities.get_failure_details(inputs=query,
                                                       expected_outputs='journey not null',
                                                       response=response)
    assert journey, failure_reason

#   D:  Given imo and canals, data is returned
@pytest.mark.parametrize('imo, origin_unlocode, destination_unlocode , canals', 
                         [(9772333, 'DEHAM', 'USNYC', 'PANAMA')],
                         ids=str)
def test_route_imo_plus_piracy(client,
                               imo,
                               origin_unlocode,
                               destination_unlocode,
                               canals):
    #  ARRANGE
    query: str = utilities.build_predicted_vessel_route_query(origin_unlocode=origin_unlocode,
                                                              destination_unlocode=destination_unlocode,
                                                              imo=imo,
                                                              canals=canals)
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    assert response
    # Should always get a journey
    journey: dict = nl('journey', response)[0]
    failure_reason: str = ''
    if not journey:
        failure_reason = utilities.get_failure_details(inputs=query,
                                                       expected_outputs='journey not null',
                                                       response=response)
    assert journey, failure_reason
