from src.utilities import get_responses, build_vessel_query
import src.constants as constants
import src.settings as settings
import src.utilities as utilities
import pytest
from nested_lookup import nested_lookup as nl

#  Purpose: Verify imo argument
#
# 1. Positive:
#    A: given imo, response will contain that imo
#    B: given a list of requested imo, only expected imo are in the result and no others > DEPRECATED AS THE ABOVE TEST NOW HANDLES THIS
# 2. Negative:
#    A: alphanum - expect null response
#    B: out of range imo like 99999999999999999999999999 - expect an error

#    A: given imo, response will contain that imo
@pytest.mark.parametrize("expected_imo", [(3), (5165776)], ids=str)
def test_imo_positive(client, expected_imo):
    #  ARRANGE
    insert = f'imo: {expected_imo}'
    query = build_vessel_query(insert=insert, segments=constants.static_data_segment)

    #  ACT
    responses, err = get_responses(connection=client,
                                   query=query,
                                   field_name='imo',
                                   limit=settings.page_limit,
                                   return_responses_only=True)
    #  ASSERT
    for response in responses:
        # get imo
        static_data: dict = nl('staticData', response)[0]
        response_imo: int = int(static_data['imo'])
        failure_reason: str = ''
        if expected_imo != response_imo:
            failure_reason = utilities.get_failure_details(inputs=query,
                                                           expected_outputs=str(expected_imo),
                                                           response=response)

            assert expected_imo == response_imo, failure_reason
        assert expected_imo == response_imo, failure_reason



#    B: given a list of requested imo, only expected imo are in the result and no others
# @pytest.mark.parametrize("expected_imo", [(3), (5165776)], ids=str)
# def test_no_unexpected_imo_in_response(client, expected_imo):
#     #  ARRANGE
#     insert = f'imo: {expected_imo}'
#     query = build_vessel_query(insert=insert, segments=constants.static_data_segment)
#
#     #  ACT
#     responses, err = get_responses(connection=client,
#                                    query=query,
#                                    field_name='imo',
#                                    limit=settings.page_limit)
#     #  ASSERT
#     assert not err
#     expected: set = set()
#     expected.add(expected_imo)
#     assert expected == set(responses), query


@pytest.mark.parametrize("bad_input, expected_error", [('hello world', constants.expected_bad_input_response)])
def test_alphanum_imo_negative(client, bad_input, expected_error):
    #  ARRANGE
    insert = f'imo: ["{bad_input}"]'
    query = build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    response: dict = dict()
    #  ACT
    responses, err = get_responses(connection=client,
                                   query=query,
                                   field_name='imo')
    #  ASSERT
    assert expected_error in err, f'GOT RESPONSES: {str(responses)[:50]}'


@pytest.mark.parametrize("bad, expected_error", [(999999999999999999999999999999999999999999,
                                                  constants.expected_value_out_of_range_response)], ids=str)
def test_imo_out_of_range_negative(client, bad, expected_error):
    #  ARRANGE
    insert: str = f'imo: {bad}'
    query = build_vessel_query(insert=insert, segments=constants.static_data_segment)

    response: dict = dict()
    error: str = ''
    #  ACT
    responses, err = get_responses(connection=client,
                                   query=query,
                                   field_name='imo')

    #  ASSERT
    assert expected_error in err, f'GOT RESPONSES: {str(responses)[:50]}'
