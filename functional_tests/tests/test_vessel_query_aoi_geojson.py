import src.constants as constants
import src.utilities as utilities
import pytest


#   PURPOSE:  Verify specified AOI as GeoJsonPolygonInput
#   POSITIVE:
#       A:  Valid GeoJsonPolygonInput, response points will be within the AOI
#   NEGATIVE:
#       B:  Invalid GeoJsonPolygonInput, response will be an error


#       A:  Valid GeoJsonPolygonInput, response points will be within the AOI
@pytest.mark.parametrize('aoi', [(constants.aoi)], ids=str)
def test_points_within_aoi(client, aoi):
    #  ARRANGE
    aoi_argument = aoi['coordinates']
    insert: str = f"""
            areaOfInterest:{{
                polygon: {{
                    type: "Polygon"
                     coordinates: {aoi_argument}
                }}
            }}
    """
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment,
                                                                  constants.last_position_update_segment])
    polygon = utilities.make_polygon(aoi)
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='lastPositionUpdate',
                                             return_responses_only=True,
                                             limit=3
                                             )
    response: dict = dict()
    for response in responses:
        last_position_update: dict = response['lastPositionUpdate']
        latitude = last_position_update['latitude']
        longitude = last_position_update['longitude']
        point = utilities.make_point(latitude=latitude, longitude=longitude)
        is_within: bool = utilities.point_is_within_aoi(point=point, polygon=polygon)
        failure_reason: str = ''
        if not is_within:
            failure_reason = utilities.get_failure_details(inputs=f'lat: {latitude}, long: {longitude}',
                                                           expected_outputs=f'WITHIN AOI\n{aoi}',
                                                           response=response)
            assert is_within, failure_reason
        assert is_within, failure_reason



#       B:  Invalid GeoJsonPolygonInput, response will be an error
@pytest.mark.parametrize('aoi, expected_error', [(constants.aoi, constants.expected_bad_input_response)], ids=str)
def test_for_error(client, aoi, expected_error):
    #  ARRANGE
    aoi_argument = aoi['coordinates']
    insert: str = f"""
            areaOfInterest:{{
                polygon: {{
                    type: "Polygon"
                     coordinates: {constants.aoi['type']} # invalid aoi
                }}
            }}
    """
    query = utilities.build_vessel_query(insert=insert, segments=[constants.last_position_update_segment])
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='lastPositionUpdate',
                                             limit=1
                                             )
    assert expected_error in err, f'QUERY: {query}\nGOT RESPONSES: {str(responses)[:100]}'