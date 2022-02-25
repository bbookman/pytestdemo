import pytest
import src.utilities as utilities
import src.constants as constants
from nested_lookup import nested_lookup as nl


#   Purpose: Verify vessel flag argument
#   POSITIVE:
#   A: Given flag are expected to be in response
#   B: No flag other than expected flag to be in response  > DEPRECATED AS THE ABOVE TEST NOW HANDLES THIS
#   NEGATIVE:
#   C: Given a non-existent flag, no data is expected
#   D: Given an incorrect type (int), error is expected
#   E: Given a flag value greater than max length returns no results


#   A: Given flag are expected to be in response
@pytest.mark.parametrize("expected_flag", [('US'), ('CN')], ids=str)
def test_good_flags(client, expected_flag):
    #  ARRANGE
    insert = f'flag: ["{expected_flag}"]'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='flag',
                                             return_responses_only=True,
                                             limit=2
                                             )
    #  ASSERT
    for response in responses:
        # get flag
        static_data: dict = nl('staticData', response)[0]
        response_flag: str = static_data['flag']
        failure_reason: str = ''
        if expected_flag != response_flag:
            failure_reason = utilities.get_failure_details(inputs=query,
                                                           expected_outputs=expected_flag,
                                                           response=response)
            assert not err
            assert expected_flag == response_flag, failure_reason
        assert not err, failure_reason
        assert expected_flag == response_flag, failure_reason


#   B: No flag other than expected flag to be in response
# @pytest.mark.parametrize('expected_flag', [('NZ'), ('MX')], ids=str)
# def test_no_unexpected_flag(client, expected_flag):
#     #  ARRANGE
#     insert = f'flag: ["{expected_flag}"]'
#     query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])
#
#     #  ACT
#     responses, err = utilities.get_responses(connection=client,
#                                              query=query,
#                                              field_name='flag',
#                                              )
#     #  ASSERT
#     for response in responses:
#         # get flag
#         static_data: dict = nl('staticData', response)[0]
#         response_flag: str = static_data['flag']
#         failure_reason: str = ''
#         if expected_flag != response_flag:
#
#     # assert not err
#     # for response in responses:
#     #     assert response == expected_flag
#

#   C: Given a bad flag, no data is expected
@pytest.mark.parametrize('bad_flag, expected_error', [('11'), ('FU')], ids=str)
def test_bad_flag(client, bad_flag, expected_error):
    #  ARRANGE
    insert = f'flag: ["{bad_flag}"]'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='flag',
                                             )
    assert not responses, f'GOT RESPONSE {str(responses)[:50]}\n{query}'


#   D: Given an incorrect type (int), error is expected
@pytest.mark.parametrize('bad_type, expected_error', [(99, constants.expected_failed_validation_error)])
def test_bad_type(client, bad_type, expected_error):
    #  ARRANGE
    insert = f'flag: [{bad_type}]'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='flag',
                                             )
    assert expected_error in err


#   E: Given a flag value greater than max length returns no results
@pytest.mark.parametrize('over_max_flag', [('AAA')], ids=str)
def test_max_flag(client, over_max_flag):
    #  ARRANGE
    insert = f'flag: ["{over_max_flag}"]'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='flag',
                                             )
    assert not responses, f'GOT RESPONSE {str(responses)[:50]}\n{query}'
