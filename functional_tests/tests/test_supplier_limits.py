import src.utilities as utilities
import src.constants as constants
import pytest
from nested_lookup import nested_lookup as nl


#   PURPOSE: verify collection type is expected given the supplier limit imposed by token
#   A: Given JAKOTA, ASTRAPAGING, or OCEANEERING token, collection type is TERRESTRIAL
#   B: Given SPIRE token, collection type is SATELLITE
#   C: Given NAVTOR, NAVTOR_B token, collection type is DYNAMIC

# JAKOTA: https://apigee.com/organizations/spire/apps/details/2200633c-2e7c-45f3-91d7-6c0b8608e513
# ASTRAPAGING: https://apigee.com/organizations/spire/apps/details/7a7570df-ff7b-47d2-b44e-31bba0ae1f36
# OCEANEERING:  https://apigee.com/organizations/spire/apps/details/3bdc0463-ee90-46ee-9206-5f52ba68e9eb
# SPIRE: https://apigee.com/organizations/spire/apps/details/858fad1f-4532-4a20-b097-eb61fe526d25
# NAVTOR: https://apigee.com/organizations/spire/apps/details/df1189bf-7e66-4f3f-a423-df1e57b6d3a4
# NAVTOR_B: https://apigee.com/organizations/spire/apps/details/f0185450-1447-4555-ad73-3792118e0eb3


@pytest.mark.parametrize('token_id, expected_collection_type',
                         [('JAKOTA', 'TERRESTRIAL'),
                          ('ASTRAPAGING', 'TERRESTRIAL'),
                          ('OCEANEERING', 'TERRESTRIAL'),
                          ('SPIRE', 'SATELLITE'),
                          ('NAVTOR', 'DYNAMIC'),
                          ('NAVTOR_B', 'DYNAMIC')],
                         ids=str)
def test_suppliers(token_id,
                   expected_collection_type,
                   url,
                   timeout,
                   retries):
    #  ARRANGE
    client = utilities.generate_client(url=url,
                                       timeout=timeout,
                                       retries=retries,
                                       token_id=token_id)
    query = utilities.build_vessel_query(
        segments=[constants.static_data_segment, constants.last_position_update_segment])
    #   ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='collectionType',
                                             limit=2,
                                             return_responses_only=True)
    #   ASSERT
    failure_reason: str = ''
    expected: set = set()
    expected.add(expected_collection_type)
    response_collection_types = set()
    response_collection_type: str = ''
    for response in responses:
        last_position_update = response['lastPositionUpdate']
        try:
            response_collection_type = nl('collectionType', last_position_update)[0]
        except IndexError:
            failure_reason = 'Did not get collectionType'
        response_collection_types.add(response_collection_type)
        if response_collection_types != expected:
            failure_reason = utilities.get_failure_details(inputs=f'token/type: {token_id} / {expected_collection_type}',
                                                           expected_outputs=expected_collection_type,
                                                           response=response)

            assert expected == response_collection_types, failure_reason
        assert expected == response_collection_types, failure_reason
