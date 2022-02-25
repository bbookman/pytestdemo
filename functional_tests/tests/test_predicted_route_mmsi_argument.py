import pytest
import src.utilities as utilities
from nested_lookup import nested_lookup as nl
import src.constants as constants


#   PURPOSE: Verify providing mmsi as arg for predicted vessel route returns results
#   - Variables under test include
#       - mmsi
#       - origin coordinates
#   NOTE:  veracity of the data is not proven, simply that some response is returned
#
#   POSITIVE:
#   A:  Given mmsi and origin coordinates, data is returned
#   NEGATIVE:
#   B:  Given mmsi and invalid coords, error is returned
#   C:  Given mmsi and invalid destination unlocode, error is returned


#   A:  Given mmsi and origin coordinates, data is returned
@pytest.mark.parametrize('mmis, origin_latitude, origin_longitude, destination_unlocode',
                         [(511576000, 18.223, 84.445, 'SGSIN')], ids=str)
def test_route_valid_mmis_all_other_args_default(client, mmis, origin_latitude, origin_longitude, destination_unlocode):
    #  ARRANGE
    query: str = utilities.build_predicted_vessel_route_query(mmsi=mmis,
                                                              destination_unlocode=destination_unlocode,
                                                              origin_latitude=origin_latitude,
                                                              origin_longitude=origin_longitude
                                                              )
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    #  ASSERT
    assert response, f'GOT NO RESPONSE.  {err}'
    # Should always get a journey
    journey: dict = nl('journey', response)[0]
    failure_reason: str = utilities.get_failure_details(inputs=f'mmsi: {mmis}\nlat: {origin_latitude}, long: {origin_longitude}\ndest: {destination_unlocode}',
                                                        response=response,
                                                        expected_outputs=f'any journey from query:\n{query}')
    assert journey, failure_reason


#   B:  GIVEN mmsi and invalid coords, error is returned
@pytest.mark.parametrize('mmis, origin_latitude, origin_longitude, destination_unlocode, expected_error',
                         [(511576000, 180.223, 84.445, 'SGSIN', constants.expected_bad_input_response)], ids=str)
def test_route_invalid_coords(client, mmis, origin_latitude, origin_longitude, destination_unlocode, expected_error):
    #  ARRANGE
    query: str = utilities.build_predicted_vessel_route_query(mmsi=mmis,
                                                              destination_unlocode=destination_unlocode,
                                                              origin_latitude=origin_latitude,
                                                              origin_longitude=origin_longitude
                                                              )
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    #  ASSERT
    assert expected_error in err, f'GOT RESPONSE: {response}'


#   C:  Given mmsi and invalid destination unlocode, error is returned
@pytest.mark.parametrize('mmis, origin_latitude, origin_longitude, destination_unlocode, expected_error',
                         [(511576000, 18.223, 84.445, 'SGSIX', constants.expected_bad_input_response)], ids=str)
def test_route_invalid_unlocode(client, mmis, origin_latitude, origin_longitude, destination_unlocode, expected_error):
    #  ARRANGE
    query: str = utilities.build_predicted_vessel_route_query(mmsi=mmis,
                                                              destination_unlocode=destination_unlocode,
                                                              origin_latitude=origin_latitude,
                                                              origin_longitude=origin_longitude
                                                              )
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    #  ASSERT
    assert expected_error in err, f'GOT RESPONSE: {response}\nquery:\n{query}'