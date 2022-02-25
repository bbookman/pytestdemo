import src.utilities as utilities
import src.constants as constants
import src.settings as settings
import pytest
from datetime import datetime

#   PURPOSE:  verify time range specifying lastposition update argument
#       POSITIVE:
#       A:  START DATE today at start of day returns data within today
#       B:  START DATE a month ago returns date up to within that date and today
#       C:  START DATE a month ago and END DATE a week ago date up to within that date and a week ago
#       NEGATIVE:
#       D:  START DATE in future returns no data
#       E: UNEXPECTED DATE FORMAT, BUT STILL A DATE: error expected
#       F: BAD TYPE: error expected


now_dt: datetime = utilities.dt_time_min(datetime.now())
one_month_ago_dt: datetime = utilities.set_date_to_days_in_past(dt=now_dt, days=28)
one_month_ago_str = utilities.datetime_to_string(dt=one_month_ago_dt)


#       A:  START DATE today at start of day returns data within today
@pytest.mark.parametrize("start_of_day_today_dt", ([now_dt]), ids=str)
def test_start_date_today(client, start_of_day_today_dt):
    #  ARRANGE
    today_str: str = utilities.datetime_to_string(start_of_day_today_dt)
    insert: str = utilities.build_last_position_update_arg(start_time=today_str)
    query = utilities.build_vessel_query(insert=insert,
                                         segments=[constants.static_data_segment, constants.last_position_update_segment])
    # #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='updateTimestamp',
                                             limit=20,
                                             return_responses_only=True)

    #  ASSERT
    failure_reason: str = ''
    for response in responses:
        last_position_update: dict = response['lastPositionUpdate']
        response_update_timestamp: str = last_position_update['updateTimestamp']
        response_dt: datetime = utilities.string_to_datetime(response_update_timestamp)
        # IF TEST FAILS, GENERATE FAILURE DETAILS
        if not response_dt > start_of_day_today_dt:
            failure_reason = utilities.get_failure_details(inputs=today_str + f'\n{query}',
                                                           expected_outputs=f'{response_dt} > {today_str}',
                                                           response=response
                                                           )
        assert response_dt > start_of_day_today_dt, failure_reason

#       B:  START DATE a month ago returns date up to within that date and today
@pytest.mark.parametrize("one_month_ago_dt, end_of_day_today",
                         ([(
                                 one_month_ago_dt,
                                 utilities.dt_time_max(dt=now_dt)
                         )]), ids=str)
def test_start_date_one_month_ago(client, one_month_ago_dt, end_of_day_today):
    #  ARRANGE

    insert: str = utilities.build_last_position_update_arg(start_time=one_month_ago_str)
    query = utilities.build_vessel_query(insert=insert,
                                         segments=[constants.last_position_update_segment])
    # #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='updateTimestamp',
                                             limit=20,
                                             return_responses_only=True)

    #  ASSERT
    failure_reason: str = ''
    for response in responses:
        last_position_update: dict = response['lastPositionUpdate']
        response_update_timestamp: str = last_position_update['updateTimestamp']
        response_dt: datetime = utilities.string_to_datetime(response_update_timestamp)
        if not response_dt <= end_of_day_today:
            node_id: str = response['id']
            static_data: dict = response['staticData']
            failure_reason = utilities.get_failure_details(inputs=f'start_time={one_month_ago_str}\n{query}',
                                                           expected_outputs=f'response: {response_dt} <= {end_of_day_today}',
                                                           response=response)
    assert response_dt <= end_of_day_today, failure_reason


#       C:  START DATE a month ago and END DATE a week ago date up to within that date and a week ago
@pytest.mark.parametrize("one_month_ago, one_week_ago_dt", [(
                                                             one_month_ago_dt,
                                                             utilities.set_date_to_days_in_past(dt=now_dt, days=7)
                                                            ),
                                                           ],
                                                            ids=str
                        )
def test_between_past_dates(client, one_month_ago, one_week_ago_dt):
    #  ARRANGE
    #  string
    one_week_ago_str: str = utilities.datetime_to_string(one_week_ago_dt)
    insert: str = utilities.build_last_position_update_arg(start_time=one_month_ago_str, end_time=one_week_ago_str)
    query = utilities.build_vessel_query(insert=insert,
                                         segments=[constants.last_position_update_segment])
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='updateTimestamp',
                                             limit=20,
                                             return_responses_only=True)
    #  ASSERT
    response_dt = None
    failure_reason: str = ''
    assert responses, 'DID NOT GET DATA'
    for response in responses:
        last_position_update: dict = response['lastPositionUpdate']
        response_update_timestamp: str = last_position_update['updateTimestamp']
        response_dt = utilities.string_to_datetime(response_update_timestamp)
        if not one_month_ago_dt <= response_dt or not one_week_ago_dt >= response_dt:
            failure_reason = utilities.get_failure_details(inputs=f'start_time={one_month_ago_str}, end_time={one_week_ago_str}\n{query}',
                                                           expected_outputs=f'{one_month_ago_dt} <= {response_dt}\n{one_week_ago_dt} >= {response_dt}',
                                                           response=response
                                                           )
        assert one_month_ago_dt <= response_dt, failure_reason
    assert one_week_ago_dt >= response_dt, failure_reason


#       D:  START DATE in future returns no data
@pytest.mark.parametrize('start_date', [utilities.set_date_to_days_in_future(dt=now_dt, days=7)], ids=str)
def test_future_start_date(client, start_date):
    start_date_str: str = utilities.datetime_to_string(dt=start_date)
    insert: str = utilities.build_last_position_update_arg(start_time=start_date_str)
    query = utilities.build_vessel_query(insert=insert,
                                         segments=[constants.last_position_update_segment])
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='updateTimestamp',
                                             limit=1)
    #  ASSERT
    assert not responses, f'GOT RESPONSES: {str(responses)[:50]}'


#       E: UNEXPECTED DATE FORMAT, BUT STILL A DATE: error expected   "%Y-%m-%dT%H:%M:%S.%fZ"
@pytest.mark.parametrize('bad_date_str, expected_err',
                         [(utilities.datetime_to_string(dt=now_dt, date_format= "%Y-%m-%dT%H:%M"),
                           constants.expected_bad_input_response)],ids=str)
def test_bad_date(client, bad_date_str, expected_err):
    insert: str = utilities.build_last_position_update_arg(start_time=bad_date_str)
    query = utilities.build_vessel_query(insert=insert,
                                         segments=[constants.last_position_update_segment])
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='updateTimestamp',
                                             limit=1)
    assert expected_err in err


#       F: BAD TYPE: error expected
@pytest.mark.parametrize('bad_date_type, expected_err', [(123, constants.expected_bad_input_response)], ids=str)
def test_bad_date_type(client, bad_date_type, expected_err):
    insert: str = utilities.build_last_position_update_arg(start_time=bad_date_type)
    query = utilities.build_vessel_query(insert=insert,
                                         segments=[constants.last_position_update_segment])
    #  ACT
    responses, err = utilities.get_responses(connection=client,
                                             query=query,
                                             field_name='updateTimestamp',
                                             limit=1)
    assert expected_err in err

