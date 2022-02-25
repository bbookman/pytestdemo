import pytest
import src.utilities as utilities
from nested_lookup import nested_lookup as nl
import src.constants as constants

#   PURPOSE: Verify port query
#   POSITIVE:
#   A:  Given a valid unlocode, data will be returned
#   NEGATIVE:
#   B:  Given a unlocode that does not exist, no data will be returned
#   C:  Given a partial unlocode, error is returned
#   D:  Given invalid unlocode, error is returned

#   A:  Given a valid unlocode, data will be returned
@pytest.mark.parametrize('unlocode, expected_name',
                         [('USNYC', "New York & New Jersey"),
                          ('DEABL', 'Abbesbuttel'),
                          ('AERUW', "AlRuwais")],
                         ids=str)
def test_valid_unlocode(client, unlocode, expected_name):
    #  ARRANGE
    query: str = utilities.build_port_query(unlocode=unlocode)

    #  ACT
    data, err = utilities.get_single_page_response(connection=client, query=query)
    #  ASSERT
    assert data, f'GOT NO RESPONSE. {err}'
    response_name = nl('name', data)[0]
    assert response_name == expected_name, f'INPUT: {unlocode}, {query}'


#   B:  Given a unlocode that does not exist, no data will be returned
@pytest.mark.parametrize('unlocode', [('USBBQ'), ('BQZAD')], ids=str)
def test_nonexistent_unlocode(client, unlocode):
    #  ARRANGE
    query: str = utilities.build_port_query(unlocode=unlocode)

    #  ACT
    data, err = utilities.get_single_page_response(connection=client, query=query)
    assert not data['port'], f'GOT DATA: {data}\n{query}'
    assert not err, query



#   C:  Given a partial unlocode, error is returned
@pytest.mark.parametrize('unlocode, expected_error',
                         [('US', constants.expected_bad_input_response),
                          ('B123', constants.expected_bad_input_response)],
                         ids=str)
def test_partial_unlocode(client, unlocode, expected_error):
    #  ARRANGE
    query: str = utilities.build_port_query(unlocode=unlocode)

    #  ACT
    data, err = utilities.get_single_page_response(connection=client, query=query)
    assert expected_error in err, f'GOT DATA: {data}\n{query}'

#   D:  Given invalid unlocode, error is returned
@pytest.mark.parametrize('unlocode, expected_error',
                         [('!@#$%', constants.expected_bad_input_response),
                          ('B111111111111', constants.expected_bad_input_response)],
                         ids=str)
def test_invalid_unlocode(client, unlocode, expected_error):
    #  ARRANGE
    query: str = utilities.build_port_query(unlocode=unlocode)

    #  ACT
    data, err = utilities.get_single_page_response(connection=client, query=query)
    assert expected_error in err, f'GOT DATA: {data}\n{query}'