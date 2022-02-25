import src.settings as settings
import src.constants as constants
import src.utilities as utilities
import pytest
from nested_lookup import nested_lookup as nl


#  Purpose: Verify mmsi argement
#
# 1. Positive:
#    A: mmsi is requested, and is expected in the response
# 2. Negative:
#    B: alphanum - expect null response
#    C: out of range mmsi like 99999999999999999999999999 - expect an error

#    A: mmsi is requested, and is expected in the response
@pytest.mark.parametrize('expected_mmsi', [(1), (563025600), (256169000)], ids=str)
def test_mmsi_positive(client, expected_mmsi):
    #  ARRANGE
    insert = f'mmsi: {expected_mmsi}'
    query = utilities.build_vessel_query(insert=insert, segments=constants.static_data_segment)
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='mmsi',
                                             limit=settings.page_limit,
                                             return_responses_only=True)
    #  ASSERT
    for response in responses:
        # get static data
        static_data: dict = nl('staticData', response)[0]
        response_mmsi: int = int(static_data['mmsi'])
        failure_reason: str = ''
        if expected_mmsi != response_mmsi:
            failure_reason = utilities.get_failure_details(inputs=expected_mmsi + f'\n{query}',
                                                           expected_outputs=str(expected_mmsi),
                                                           response=response)
            assert expected_mmsi == response_mmsi, failure_reason
        assert expected_mmsi == response_mmsi, failure_reason


#    A: alphanum - expect null response
@pytest.mark.parametrize('bad_mmsi, expected_error', [('aX2', constants.expected_bad_input_response)], ids=str)
def test_alphanum_mmsi_negative(client, bad_mmsi, expected_error):
    #  ARRANGE
    insert = f'mmsi: {bad_mmsi}'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='mmsi')
    #  ASSERT
    assert expected_error in err


#    B: out of range mmsi like 99999999999999999999999999 - expect null response
@pytest.mark.parametrize('out_of_rage_mmsi, expected_error',
                         [(99999999999999999999999999, constants.expected_value_out_of_range_response)],
                         ids=str)
def test_mmsi_out_of_range_negative(client, out_of_rage_mmsi, expected_error):
    #  ARRANGE
    out_of_range_mmsi: int = 9999999999999999999
    insert: str = f'mmsi: {out_of_range_mmsi}'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                   query=query,
                                   field_name='mmsi')
    #  ASSERT
    assert expected_error in err
