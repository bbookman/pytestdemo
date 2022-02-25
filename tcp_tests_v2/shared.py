from enum import Enum

"""
jira_project_id: running a test will add a new issue to the project set
epic_id : An epic must exist to add the generated issues, this take the epic id
update_jira: Set to False if you want to debug tests and not create issues in Jira

"""
jira_project_key = 'MDO'
epic_id = '41996'
update_jira = True

class Tokens(Enum):
    sat_down_v2 = "wQ9QZEoLcs6UCZQC5XnL6vB85VjpUyAY"
    sat_down_v1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lciI6eyJpZCI6Ijg5MyIsIm5hbWUiOiJTQVRfT05MWSIsInV1aWQiOiI4OTMifSwiaXNzIjoic3BpcmUuY29tIiwiaWF0IjoxNjE2MDM0ODU2fQ.v6OOCqJSi7ZpKNUkHsRgRGp9f4HAJ4TBB-RCsSA21GE"
    full_v2 = "AqjxBiI615ihxrAQX1dUJmBIAfRUvI87"
    down_v2 = "v5kv3vPShITK9JRjyNbTUis6S9d6pG9o"
    full_v2_no_s_tags = "mMUwL2dNQgPfbudqHMijeVxrjh3weU9s"
    down_v2_no_s_tags = "L536rrNOZbsjnOOhgvHHez8G4d8GSLE3"
    full_v2_no_g_tags = "6SDY4DrAXhKpnx1zuwLtTotZcAtqCRkk"
    down_v2_no_g_tags = "Jna5NXt1cZgnZtA7LI6SwOND6gEJhcJy"
    full_v2_no_terrestrial = "txX320idDCBrBlGtahsd5FKZfI2baVbx"
    full_v2_no_astrapaging = "Gx8cqpmiFhtlE5CR1Lc3DkivxQMud2Ce"
    down_v2_no_astrapaging = "YSRnm1lKUnbOY8dFlAudgTA6W0KuFD3L"
    full_v2_no_jakota = "P2AmAj50oRccVuXxONBxjBL7ukAHCGWC"
    down_v2_no_jakota = "8iHwRvfcRWqbFyrdWXGN4stRf8hKlhjl"
    down_v2_sat_only_no_norad = "35EoMIog1BCzpavqEALZ98cH1N2mxSsN"
    full_v2_no_spire = "tQm2L4gBh3tzV0mZdniq8ZYjEcW9PFLb"
    down_v2_no_spire = "u37LYIS52OUIVa5Gzj8TbxvfM1BbanVD"
    full_v2_no_navtor = "mZtBgWNWAMI1NyYmovXjeg38wLuGl2sG"
    down_v2_no_navtor = "OA2cCAwKuKxFw6tgxMnK3EVmQ0oZzTAS"
    down_v2_no_navtor_no_navtor_b = "jLczNTLkP7rZZGeBaFcFlLVTEhIL0WxF"
    full_v2_no_oceaneering = "GEsJXInKffDcpuDCzwowUd7djX1eTTuS"
    down_v2_no_oceaneering = "czsuRYtYVxBf6ed3x1qkr2Di1pno3Oap"
    down_v2_sat_terrestrial = "9uIll3aCCc8GRMm6WHYpJI4aVWPAtJPG"
    quietoceans_v2 = "qtJH2SmEoGqzpaEFgI8BkqJAw0hus41X"

class Ports(Enum):
    v2_production = 56784
    v2_staging = 25000
    v1_production = 56784


class Endpoints(Enum):
    v2_production = "streamingv2.ais.spire.com"
    v1_production = "streaming.ais.spire.com"
    v2_staging = "awseb-AWSEB-16Y677R5QWSUW-92f60b188e4e05af.elb.us-west-2.amazonaws.com"


"""
!!!       DO NOT EDIT   !!!
"""
all_ais_fields = ['id', 'eta_minute', 'special_manoeuvre', 'speed_qual', 'band_flag', 'txrx_mode', 'dest_mmsi', 'seq_num', 'course_qual', 'y', 'msg_2', 'cur_dir_3', 'offset_b', 'fi', 'x1', 'ship_type', 'eta_hour', 'mode_flag', 'slot_offset_2', 'horz_vis', 'ais_version', 'cog', 'received_stations_valid', 'received_stations', 'chan_a', 'display_flag', 'true_heading', 'month', 'wind_dir', 'reservations', 'swell_period', 'eta_day', 'wind_ave', 'm22_flag', 'wave_period', 'unit_flag', 'swell_dir', 'part_num', 'dac', 'aton_type', 'slot_number', 'zone_size', 'slot_increment_valid', 'dest_mmsi_valid', 'eu_id', 'spare4', 'commstate_flag', 'slot_offset', 'addressed', 'chan_b_bandwidth', 'aton_status', 'assigned_mode', 'mmsi_1', 'imo_num', 'msg_1_1', 'req_dac', 'water_level', 'utc_valid', 'dim_b', 'draught', 'power_low', 'keep_flag', 'rot_over_range', 'fix_type', 'loaded', 'gnss', 'spare', 'utc_spare', 'cur_dir_2', 'slot_offset_valid', 'use_app_id', 'text', 'air_pres_trend', 'salinity', 'slot_offset_1_2', 'inc_a', 'y1', 'vendor_id', 'time_stamp', 'heading_qual', 'utc_min', 'cur_speed_3', 'x2', 'dsc_flag', 'dest_msg_1_2', 'sog', 'year', 'y2', 'second', 'mmsi', 'seq', 'wind_gust', 'retransmitted', 'offset_a', 'timestamp', 'acks', 'surf_cur_speed', 'slots_to_allocate', 'retransmit', 'inc_b', 'station_type', 'air_pres', 'alt_sensor', 'nav_status', 'water_level_trend', 'dim_c', 'ice', 'eta_month', 'slot_number_valid', 'dte', 'x', 'sync_state', 'dim_a', 'wave_height', 'sea_state', 'callsign', 'voltage', 'cur_depth_2', 'keep_flag_valid', 'air_temp', 'transmission_ctl', 'mmsi_2', 'spare3', 'dew_point', 'beam', 'commstate_cs_fill', 'dim_d', 'virtual_aton', 'chan_b', 'precip_type', 'interval_raw', 'repeat_indicator', 'haz_cargo', 'water_temp', 'slot_timeout', 'position_accuracy', 'wave_dir', 'utc_hour', 'length', 'spare2', 'hour', 'dest_mmsi_b', 'quiet', 'slot_increment', 'surf_cur_dir', 'slot_offset_1_1', 'utc_day', 'off_pos', 'cur_depth_3', 'type_and_cargo', 'rel_humid', 'slot_timeout_valid', 'wind_gust_dir', 'slots_to_allocate_valid', 'cur_speed_2', 'sub_id', 'minute', 'swell_height', 'spare_2', 'chan_a_bandwidth', 'alt', 'name', 'raim', 'rot', 'mmsi_dest', 'dest_mmsi_a', 'day']

line_count = 0




