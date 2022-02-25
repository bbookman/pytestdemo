import os
from gql import gql
from copy import deepcopy
from datetime import datetime, time, timedelta
from rfc3339 import rfc3339
from shapely.geometry import Point, shape, Polygon
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from nested_lookup import nested_lookup as nl


def build_vessel_query(insert: str = '', segments: list = [], first: int = 1000):
    """Builds the vessels query

    Args:
        insert: string containing query arguments and values for inclusion in query
        segments: string building blocks for the query body
        first: integer specifying teh number of nodes to return per page
    Returns:
        query string
    """
    query: str = f"""
    query {{
          vessels(first: {first} {insert}) {{
            pageInfo {{
              hasNextPage
              endCursor
            }}
            nodes{{
              id
    """
    if segments:
        for segment in segments:
            query += segment
    #  close all brackets
    query += """
        } # nodes
      } #vessel
    } # query
    """
    return query


def single_quotes_to_double_quotes(string_list: list):
    """Converts single quoted strings into double quoted

    If Python strings a list, it ignores the original quotes and makes all members single quoted

    Args:
        string_list: list of single quoted strings

    Returns:
        list of double quoted strings
    """
    result: str = ''
    for i in string_list:
        result += f'"{i}",'
    return result


def page(connection, query, limit: int):
    """Pages through response

    Args:
        connection: gql connection
        query: string query
        limit: number of pages to process, helpful for large results body

    Returns:
        list with response dictionaries
        error string if an error occurs - may be expected upstream
    """
    results: list = list()
    original_query = deepcopy(query)
    page_count = 0
    while True:
        response: dict = dict()
        err: str = ''
        response, err = get_single_page_response(connection=connection, query=query)
        page_count += 1
        # get just the nodes
        data_list: list = nl('nodes', response)
        try:
            nodes: list = data_list[0]
        except IndexError:
            # no more nodes
            return results, err
        results.extend(nodes)
        #  get cursor
        cursor: str = nl('endCursor', response)[0]
        if not cursor:
            return results, err
        else:
            if limit and page_count >= limit:
                return results, err
            insert_text = f'after: "{cursor}"'
            query = insert_into_query_args(insert_text=insert_text, query=original_query)


def insert_into_query_args(query, insert_text=''):
    """Inserts text into the query argements section

    Args:
        query: query string
        insert_text: string to insert

    Returns:
        string
    """
    if ')' in query:
        loc = query.find(')')
        # remove the existing )
        tmp: str = query.replace(')', '')
        # add paging elements where the ) once was .. + 1 for some spacing in case
        beginning: str = tmp[:loc]
        end: str = tmp[loc:]
        new_query: str = beginning + ' ' + insert_text + ' ) ' + end
    else:
        return query
    return new_query


def get_responses(connection, query, field_name, limit=0, return_responses_only: bool = False):
    """Gets a response for a query
    Args:
        connection: gql clinet
        query:  text gql query
        field_name: name of field / column for the value of interest
        limit:  number of pages to process
        return_responses_only: if True, the field name will be ignored
        and the entire list of responses will be returned.

    Returns:
        A list of responses
    """
    responses, err = page(connection=connection, query=query, limit=limit)
    if return_responses_only:
        return responses, err
    results: list = list()
    for response in responses:
        if field_name == 'lastPositionUpdate':
            #  Could be null, so ignore
            last_position_update: dict = nl(field_name, response)[0]
            if last_position_update:
                lat = nl('latitude', last_position_update)[0]
                long = nl('longitude', last_position_update)[0]
                results.append([lat, long])
        else:
            value: list = nl(field_name, response)
            if value:
                results.extend(value)
    return results, err


def string_to_datetime(string):
    """ Converts string to time zone naive datetime

    Args:
        string: the string to convert to datetime

    Returns:
        time zone naive datetime
    """
    from dateutil.parser import parse
    dt_obj_w_tz = parse(string)
    dt_obj_wo_tz = dt_obj_w_tz.replace(tzinfo=None)
    return dt_obj_wo_tz


def datetime_to_string(dt=datetime.now(), date_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"):
    """Converts datetime to string

    Args:
        dt: a datetime, defaults to now at beginning of day
        date_format: format for string

    Returns:
        string
    """
    # current date and time
    dt = dt_time_min(dt)
    date_time = dt.strftime(date_format)
    return date_time


def dates_are_within_range(start_date, end_date):
    """Determines if an end date is >= start date

    Args:
        start_date: datetime
        end_date: datetime

    Returns:
        bool
    """
    if type(start_date) == str:
        start_date = rfc3339(start_date)
    if type(end_date) == str:
        end_date = rfc3339(end_date)
    return end_date >= start_date


def dt_time_min(dt):
    """converts any datetime/date to new datetime with same date and time=0:00:00
    Sets the time component to zeros
    """
    minimized = datetime.combine(dt, time.min)
    return minimized


def dt_time_max(dt):
    """converts any datetime/date to new datetime with same date and time=23:59:59.999999
    Sets the time component to the end of the day
    """
    return datetime.combine(dt, time.max)


def build_last_position_update_arg(start_time: str = '', end_time: str = ''):
    """Makes lastPositionUpdate argument for inserting into query

    Args:
        start_time: string for time range of query
        end_time: string for time range of query

    Returns:
        string

    """
    result: str = f"""
           lastPositionUpdate:{{
               startTime: "{start_time}"
       """
    if end_time:
        result += f'endTime: "{end_time}"'
    result += '}'

    return result


def set_date_to_days_in_past(dt: datetime, days: int):
    """Sets datetime back X days

    Args:
        dt: datetime to set to the past
        days: int number of days

    Returns:
        datetime

    """
    return dt - timedelta(days=days)


def set_date_to_days_in_future(dt: datetime, days: int):
    """Sets date to number of days in the future

    Args:
        dt: datetime to set into the future
        days: int number of days

    Returns:
        datetime
    """
    return dt + timedelta(days=days)


def build_port_query(unlocode: str):
    """Creates a port query

    Args:
        unlocode: string for unlocode

    Returns:
        query string

    """
    result = f"""
    query {{
            port(
                unlocode: "{unlocode}"
            ){{
                name
                unlocode
                centerPoint{{
                    latitude
                    longitude
                }} # centerpoint
          }} # port
    }}  # query
    """
    return result


def build_predicted_vessel_route_query(destination_unlocode: str = '',
                                       origin_unlocode: str = '',
                                       origin_latitude: float = 0.0,
                                       origin_longitude: float = 0.0,
                                       imo: int = 0,
                                       mmsi: int = 0,
                                       piracy='false',
                                       canals='',
                                       speed: float = 0.0,
                                       ):
    """
            Args:
                destination_unlocode: required destination unlocode
                origin_unlocode: optional origin unlocode
                origin_latitude: optional origin latitude
                origin_longitude: optional origin longitude
                imo: optional vessel imo
                mmsi: optional vessel mmsi
                piracy: false by default  (or true lower case)
                canals: optional, list of canal route options
                speed: optional vessel speed

            Returns:
                query string
            """

    # open query
    q: str = 'query { '
    # add piracy
    q += f"""predictedVesselRoute( piracy: {piracy.lower()} """
    # open vessel
    q += 'vessel: { '
    # add either mmsi and or imo
    if imo:
        q += f""" imo: {imo} """

    if mmsi:
        q += f""" mmsi: {mmsi} """
    # close vessel
    q += '}'

    # add origin

    if (origin_latitude and origin_longitude) and not origin_unlocode:
        q += f"""
                       origin:{{
                         coordinates:{{
                           latitude: {origin_latitude}
                           longitude: {origin_longitude}
                         }}
                       }}
               """
    elif origin_unlocode and not (origin_latitude or origin_longitude):
        q += f"""
                       origin:{{
                         unlocode:{origin_unlocode}
                       }}
               """
    q += f""" destination: {{ unlocode: {destination_unlocode}}}  """

    if canals:
        q += f""" canals: [{canals}] """
    if speed:
        q += f""" speed: {speed} """

    q += ')'  # end input

    q += """
             {
        journey {
          ...RouteDetails
        }
        itinerary {
          ...RouteDetails
        }
      }
    }
    # fragment PortDetails on Port {
    #   name
    #   unlocode
    #   centerPoint {
    #     latitude
    #     longitude
    #   }
    # }

    fragment RouteDetails on VesselRoute {
      distance
      duration {
        seconds
        iso
        text
      }
      eta
      seca
      # destinationPort {
      #   ...PortDetails
      # }
      # origin {
      #   ...PortDetails
      # }
      waypoints {
        wkt
        geoJson {
          coordinates
          type
        }
      }
    }
            """
    return q


def get_single_page_response(connection, query: str = ''):
    """Gets a single page response from service endpoint

    Args:
        connection: graphQL client
        query: string to submit as query

    Returns:
        response dictionary
        error string
    """
    response: dict = dict()
    err: str = ''
    try:
        response = connection.execute(gql(query))
    except Exception as e:
        err = str(e.args[0])
    return response, err


def build_matched_port_query(text: str):
    """Creates a matchedPort query

    Args:
        text: string to match for the port

    Returns:
        query string
    """
    q = f"""
    query{{
        matchedPort(text: "{text}")
            {{
                port{{
                    name
                    unlocode
                    centerPoint{{
                        latitude
                        longitude
                    }}    
                }}
            }}
    }}
    """
    return q


def make_polygon(aoi: dict):
    """Creates a shapely polygon

    Args:
        aoi: Geo dictionary

    Returns:
        shapely polygon

    """
    polygon: Polygon = shape(aoi)
    return polygon


def make_point(latitude, longitude):
    """Makes a shapely point

    Args:
        latitude: float
        longitude: float

    Returns:
        shapely point

    """
    #  Latitude is the Y axis, longitude is the X axis
    point = Point(longitude, latitude)
    return point


def point_is_within_aoi(point: Point, polygon: shape):
    """Determines if given point is within polygon

    Args:
        point: shapely point
        polygon: shapely polygon (shape)

    Returns:
        bool

    """
    _point = point
    _polygon = polygon
    is_within = bool(_point.within(_polygon))
    return is_within


def generate_client(url, timeout, retries, token_id: str = 'TOKEN_ALL_PRODUCTS_NO_RESTRICTIONS'):
    """Creates a graphQL client

    Args:
        url: endpoint string
        timeout: int
        retries: int
        token_id: string for bearer token

    Returns:
        gql client
    """
    if token_id == 'bad_token':
        token = token_id
    else:
        token = get_vault_token(token_id=token_id)
    headers: dict = dict()
    headers['Authorization'] = f'Bearer {token}'
    transport = RequestsHTTPTransport(
        url=url,
        headers=headers,
        retries=retries,
        timeout=timeout
    )
    c = None
    try:
        c = Client(transport=transport)
    except Exception as e:
        pass
    return c


def get_vault_token(token_id: str):
    """Get the token string from environment
    returns: token as string
    """
    token: str = os.environ[token_id]
    return token


def get_failure_details(inputs: str = '',
                        expected_outputs: str = '',
                        response: dict = dict()
                        ):
    """

    Args:
        inputs: test inputs as string
        expected_outputs: expected outputs or notes as string
        response: full gql response dictionary

    Returns:
        detailed failure string
    """

    return_string: str = f"""
    INPUTS: {inputs}
    EXPECTED OUTPUTS: {expected_outputs} 
    """
    static_data: dict = dict()
    last_position_update: dict = dict()
    port: dict = dict()
    matched_port = dict()
    node_id: str = ''
    predicted_vessel_route: dict = dict()
    try:
        static_data = response['staticData']
    except KeyError:
        pass
    try:
        last_position_update = response['lastPositionUpdate']
    except KeyError:
        pass
    try:
        port = response['port']
    except KeyError:
        pass
    try:
        matched_port = response['matchedPort']
    except KeyError:
        pass
    try:
        node_id = response['id']
    except KeyError:
        pass
    try:
        predicted_vessel_route = response['predictedVesselRoute']
    except KeyError:
        pass

    if static_data:
        mmsi: str = static_data['mmsi']
        imo: str = static_data['imo']
        ship_type: str = static_data['shipType']
        ship_name: str = static_data['name']
        return_string += f"""
        node_id: {node_id}
        mmsi: {mmsi}
        imo: {imo}
        name: {ship_name}
        type: {ship_type}"""
    if last_position_update:
        latitude: str = last_position_update['latitude']
        longitude: str = last_position_update['longitude']
        update_timestamp: str = last_position_update['updateTimestamp']
        timestamp: str = last_position_update['timestamp']
        return_string += f"""
        lastPositionUpdate:
           latitude: {latitude}
           longitude: {longitude}
           timestamp: {timestamp}
           updateTimestamp: {update_timestamp}
        """
    if port:
        return_string += f'port_data: {port}'
    if matched_port:
        return_string += f'matched_port: {matched_port}'
    if predicted_vessel_route:
        journey: dict = dict()
        try:
            journey = predicted_vessel_route['journey']
        except KeyError:
            pass
        return_string += f'JOURNEY: {str(journey)[:50]}'

    return return_string
