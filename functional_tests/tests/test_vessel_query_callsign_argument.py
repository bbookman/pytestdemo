from src.utilities import build_vessel_query, get_responses
import src.constants as constants
import src.settings as settings
import src.utilities as utilities
import pytest

#   Purpose: Verify callsign argement
#   Positive:
#       A: valid call sign list
#   Negative:
#       B: invalid call sign type
#       C: empty call sign


#       A: valid call sign list
@pytest.mark.parametrize("expected_callsign",[("V7mg8"), ("bOAG9"), ("VRkL3")], ids=str)
def test_valid_callsigns_positive(client, expected_callsign):
    #  ARRANGE
    insert: str = f'callsign: ["{expected_callsign}"]'
    query = build_vessel_query(insert=insert, segments=[constants.static_data_segment])
    #  ACT
    responses, err = get_responses(connection=client,
                                   query=query,
                                   field_name='callsign',
                                   limit=settings.page_limit,
                                   return_responses_only=True)
    for response in responses:
        response_call_sign: str = response['staticData']['callsign']
        failure_reason: str = ''
        if expected_callsign.upper() != response_call_sign:
            failure_reason = utilities.get_failure_details(inputs=query,
                                                           expected_outputs=expected_callsign,
                                                           response=response)
        assert not err
        assert expected_callsign.upper() == response_call_sign, failure_reason




#       B: invalid call sign type
@pytest.mark.parametrize("bad, expected_error", [(1, constants.expected_failed_validation_error)
                                              ,(9876, constants.expected_failed_validation_error)]
                                            ,ids=str)
def test_wrong_type(client, bad, expected_error):
    #  ARRANGE
    insert: str = f'callsign: {bad}'
    query = build_vessel_query(insert=insert, segments=constants.static_data_segment)
    #  ACT
    responses, err = get_responses(connection=client,
                                   query=query,
                                   field_name='callsign')
    #  ASSERT
    assert expected_error in err, query


#       C: empty call sign
@pytest.mark.parametrize("invalid, expected_error", [("", constants.expected_syntax_error)], ids=str)
def test_invalid_callsign(client, invalid, expected_error):
    #  ARRANGE
    insert: str = f'callsign: {invalid}'
    query = build_vessel_query(insert=insert, segments=constants.static_data_segment)
    #  ACT
    responses, err = get_responses(connection=client,
                                   query=query,
                                   field_name='callsign')
    #  ASSERT
    assert expected_error.lower() in err.lower(), query