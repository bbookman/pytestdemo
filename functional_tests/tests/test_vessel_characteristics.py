import pytest
import src.utilities as utilities
import src.constants as constants
import src.settings as settings


#   PURPOSE - Ensure characteristics are returned given imo, mmis
#   NOTES:
#       imo, mmsi obtained via SQL table
#       assumed that these do produce characteristics, but MAY not
#
#       the test will NOT verify the data for accuracy
#
#   POSITIVE:
#   A:  given imo, characteristic data is returned
#   B:  givem mmsi, characteristic data is returned


@pytest.mark.parametrize("given_imo", [(9120853),(9809643), (9340984),])
def test_imo_arg(client, given_imo):
    #  ARRANGE
    insert: str = f'imo: {given_imo}'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.characteristics_extended_segment])
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='imo',
                                             limit=settings.page_limit,
                                             return_responses_only=True)
    #  ASSERT
    characteristics: dict = dict()
    try:
        characteristics = responses[0]['characteristics']
    except IndexError:
        pass
    assert characteristics, f'QUERY THAT FAILS: \n{query}'


@pytest.mark.parametrize("given_mmsi", [(538008520), (533132087), (636019548)], ids=str)
def test_mmsi_arg(client, given_mmsi):
    #  ARRANGE
    insert: str = f'mmsi: {given_mmsi}'
    query = utilities.build_vessel_query(insert=insert, segments=[constants.characteristics_extended_segment])
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='mmsi',
                                             limit=settings.page_limit,
                                             return_responses_only=True)
    #  ASSERT
    characteristics: dict = dict()
    try:
        characteristics = responses[0]['characteristics']
    except IndexError:
        pass
    assert characteristics, f'QUERY THAT FAILS: \n{query}'

