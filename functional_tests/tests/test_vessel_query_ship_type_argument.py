import pytest
import src.utilities as utilities
import src.constants as constants
from nested_lookup import nested_lookup as nl
import src.settings as settings


#   Purpose: Verify vessel ship type argument
#   POSITIVE:
#   A: Given ship types are expected to be in response
#   B: No ship type other than expected type to be in response > DEPRECATED AS THE ABOVE TEST NOW HANDLES THIS
#   NEGATIVE:
#   C: Given a bad ship type, error is expected
#   D: Given an incorrect type (int), error is expected


#   A: Given ship types are expected to be in response
@pytest.mark.parametrize("expected_ship_type", [('CONTAINER'), ('FISHING'), ('OTHER')], ids=str)
def test_good_ship_types(client, expected_ship_type):
    #  ARRANGE
    insert = f'shipType: [{expected_ship_type}]'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='shipType',
                                             return_responses_only=True,
                                             limit=settings.page_limit)
    #   ASSERT
    for response in responses:
        failure_reason: str = ''
        # get static data
        static_data: dict = nl('staticData', response)[0]
        # get shipType
        response_ship_type: str = static_data['shipType']
        if expected_ship_type != response_ship_type:
            failure_reason = utilities.get_failure_details(inputs=expected_ship_type + f'\n{query}',
                                                           expected_outputs=expected_ship_type,
                                                           response=response)
            assert not err
            assert expected_ship_type == response_ship_type, failure_reason
        assert expected_ship_type == response_ship_type, failure_reason


#   B: No ship type other than expected type to be in response
# @pytest.mark.parametrize("expected_ship_type", [('TANKER_CRUDE'), ('OFFSHORE'), ('LNG_CARRIER')], ids=str)
# def test_no_unexpected_ship_types(client, expected_ship_type):
#     #  ARRANGE
#     insert = f'shipType: [{expected_ship_type}]'
#     query = build_vessel_query(insert=insert, segments=[constants.static_data_segment])
#
#     #  ACT
#     responses, err = get_responses(connection=client,
#                                    query=query,
#                                    field_name='shipType')
#
#     assert not err
#     for response in responses:
#         assert response == expected_ship_type


#   C: Given a bad ship type, error is expected
@pytest.mark.parametrize('bad_ship_type, expected_error', [('NOT_CARGO', constants.expected_failed_validation_error),
                                                           ('123', constants.expected_failed_validation_error)],
                         ids=str)
def test_bad_ship_type(client, bad_ship_type, expected_error):
    #  ARRANGE
    insert = f'shipType: [{bad_ship_type}]'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='shipType')
    #  ASSERT
    assert expected_error in err, f'GOT RESPONSE: {str(responses)[:50]}'


#   D: Given an incorrect type (int), error is expected
@pytest.mark.parametrize('bad_data_type, expected_error', [(1, constants.expected_failed_validation_error)], ids=str)
def test_bad_data_type(client, bad_data_type, expected_error):
    insert = f'shipType: [{bad_data_type}]'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='shipType')
    #  ASSERT
    assert expected_error in err, f'GOT RESPONSE: {str(responses)[:50]}'
