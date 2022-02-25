import src.constants as constants
import src.utilities as utilities
import pytest

# Purpose: Verify authentication
# 1. Positive authentication using gql client expecting return value
# 2. Negative authentication expecting 'FORBIDDEN'


# 1. Positive authentication using gql client expecting return value
def test_authentication_positive(client):
    #  ARRANGE
    query = utilities.build_vessel_query(segments=[constants.static_data_segment])
    #  ACT
    responses, err = utilities.get_single_page_response(connection=client,
                                                        query=query)

    #  ASSERT
    assert not err, f'GOT ERROR: {err}'
    assert responses, f'DID NOT GET RESPONSE\n{query}'


# 2. Negative authentication expecting 'FORBIDDEN'
@pytest.mark.parametrize('bad_token, expected_err', [('bad_token', constants.expected_bad_token_response)])
def test_authentication_negative(bad_token, expected_err, url, retries, timeout):
    #  ARRANGE
    query = utilities.build_vessel_query(segments=[constants.static_data_segment])
    response: dict = dict()
    error: str = ''
    bad_client = utilities.generate_client(url=url,
                                           retries=retries,
                                           timeout=timeout,
                                           token_id='bad_token')

    #  ACT
    responses, err = utilities.get_single_page_response(connection=bad_client,
                                                        query=query)

    #  ASSERT
    assert expected_err in err, f'DID NOT GET EXPECTED ERROR: {constants.expected_bad_token_response}'
    assert not response, f'GOT UNEXPECTED RESPONSE: {responses}\n{query}'

