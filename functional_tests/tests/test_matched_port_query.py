import pytest
import src.utilities as utilities
import src.constants as constants
from nested_lookup import nested_lookup as nl


#   PURPOSE: Validate matchedPort query - returned data is not validated
#   POSITIVE:
#   A:  Given valid text, matchedPort is returned
#   NEGATIVE:
#   B:  Given text < 2 char, err is returned
#   C:  Given a port that does not exist, no data is returned


#   A:  Given valid text, matchedPort is returned
@pytest.mark.parametrize('text, expected_unlocode', [('hello', 'NOHLE'), ('fe', 'DKFEJ'), ('zz', 'ZWZMZ')], ids=str)
def test_valid_input_for_matched_port(client, text, expected_unlocode):
    #  ARRANGE
    query: str = utilities.build_matched_port_query(text=text)
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    #  ASSERT
    response_unlocode = nl('unlocode', response)[0]
    failure_reason: str = ''
    if not expected_unlocode == response_unlocode:
        failure_reason = utilities.get_failure_details(inputs=text,
                                                       expected_outputs=expected_unlocode,
                                                       response=response)

    assert expected_unlocode == response_unlocode, failure_reason


#   B:  Given text < 2 char, err is returned
@pytest.mark.parametrize('text, expected_error', [('a', constants.expected_bad_input_response),
                                                  ('z', constants.expected_bad_input_response)],
                         ids=str)
def test_invalid_input_for_matched_port(client, text, expected_error):
    #  ARRANGE
    query: str = utilities.build_matched_port_query(text=text)
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    #  ASSERT
    assert expected_error in err, f'DID NOT GET ERROR. QUERY: {query}'


#   C:  Given a port that does not exist, no data is returned
@pytest.mark.parametrize('text, expected_port_value', [('111', 'None')], ids=str)
def test_non_existent_port_for_matched_port(client, text, expected_port_value):
    #  ARRANGE
    query: str = utilities.build_matched_port_query(text=text)
    #  ACT
    response, err = utilities.get_single_page_response(connection=client, query=query)
    #  ASSERT
    failure_reason: str = ''
    response_port_value = nl('port', response)[0]
    if not expected_port_value == str(response_port_value):
        failure_reason = utilities.get_failure_details(inputs=text,
                                                       expected_outputs=expected_port_value,
                                                       response=response)

    assert expected_port_value == str(response_port_value), failure_reason + f'\n{query}'
