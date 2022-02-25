import src.utilities as utilities
import src.settings as settings
import src.constants as constants
from nested_lookup import nested_lookup as nl
import pytest


# Purpose: Verify vessel name argument
# Names are strictly matched, there is no fuzzy matching
# Positive:
#    A: List of vessel names is requested, verify strict matching
# Negative:
#    B: Providing no name produces empty response
#    C: Providing wrong type (int) produces null data response


#    A: List of vessel names is requested, verify strict matching
@pytest.mark.parametrize("good_name", ["A", "QueeN", "kinG", "1"], ids=str)
def test_vessel_names_positive(client, good_name):
    #  ARRANGE
    insert: str = f'name: ["{good_name}"]'
    query = utilities.build_vessel_query(insert=insert, segments=constants.static_data_segment)

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='name',
                                             limit=settings.page_limit,
                                             return_responses_only=True)
    #  ASSERT
    for response in responses:
        failure_reason: str = ''
        # get static data
        static_data: dict = nl('staticData', response)[0]
        # get response name
        response_name: str = static_data['name']
        if good_name.upper() != response_name.upper():
            failure_reason = utilities.get_failure_details(inputs=good_name + f'\n{query}',
                                                           expected_outputs=good_name,
                                                           response=response)
            assert good_name.upper() == response_name.upper(), failure_reason
        assert good_name.upper() == response_name.upper(), failure_reason


#  B: Providing no name produces empty response
@pytest.mark.parametrize("no_name, expected_error", [('', constants.expected_syntax_error)], ids=str)
def test_no_name_negative(client, no_name, expected_error):
    #  ARRANGE
    insert: str = f'name: {no_name}'
    query = utilities.build_vessel_query(insert=insert, segments=constants.static_data_segment)
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='name')
    #  ASSERT
    assert expected_error.lower() in err.lower(), str(responses)[:50]


#    C: Providing wrong type (int) produces null data response
@pytest.mark.parametrize('bad_name, expected_error', [(1, constants.expected_failed_validation_error)], ids=str)
def test_wrong_type_negative(client, bad_name, expected_error):
    insert: str = f'name: [{bad_name}]'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.static_data_segment])

    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='name')
    assert not responses
    assert expected_error in err, str(responses)[:50]
