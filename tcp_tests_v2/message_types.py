
type_dict = {
    '1' : {
        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "nav_status": int,
        "rot_over_range": bool,
        "rot": float,
        "sog": float,
        "position_accuracy": int,
        "x": float,
        "y": float,
        "cog": float,
        "true_heading": int,
        "timestamp": int,
        'special_manoeuvre': int,
        "spare": int,
        "raim": bool,
        "sync_state": int,
        "slot_timeout": int,
        "slot_number": int,
        "received_stations": int,
        "slot_offset": int,
    },

    '2': {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "nav_status": int,
        "rot_over_range": bool,
        "rot": float,
        "sog": float,
        "position_accuracy": int,
        "x": float,
        "y": float,
        "cog": float,
        "true_heading": int,
        "timestamp": int,
        'special_manoeuvre': int,
        "spare": int,
        "raim": bool,
        "sync_state": int,
        "slot_timeout": int,
        "slot_number": int,
        "received_stations": int,
        "slot_offset": int,

    },

    '3' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "nav_status": int,
        "rot_over_range": bool,
        "rot": float,
        "sog": float,
        "position_accuracy": int,
        "x": float,
        "y": float,
        "cog": float,
        "true_heading": int,
        "timestamp": int,
        'special_manoeuvre': int,
        "spare": int,
        "raim": bool,
        "sync_state": int,
        "slot_timeout": int,
        "slot_number": int,
        "received_stations": int,
        "slot_offset": int,
        "slot_increment": int,
        "keep_flag": bool,
        "slots_to_allocate": int,

    },

    '4' : {

        "id": int,
        "mmsi": int,
        "year": int,
        "month": int,
        "day": int,
        "hour": int,
        "minute": int,
        "second": int,
        "position_accuracy": int,
        "x": float,
        "y": float,
        "fix_type": int,
        "transmission_ctl": int,
        "spare": int,
        "raim": bool,
        "repeat_indicator": int,
        "sync_state": int,
        "slot_timeout": int,
        "utc_hour": int,
        "utc_min": int,
        "utc_spare": int,
        "received_stations": int,
        "slot_number": int
    },

    '5': {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "ais_version": int,
        "imo_num": int,
        "callsign": str,
        "name": str,
        "type_and_cargo": int,
        "dim_a": int,
        "dim_b": int,
        "dim_c": int,
        "dim_d": int,
        "fix_type": int,
        "eta_month": int,
        "eta_day": int,
        "eta_hour": int,
        "eta_minute": int,
        "draught": int,
        "dte": str,
        "spare": bool
    },

    '6' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "seq": int,
        "mmsi_dest": int,
        "retransmit": bool,
        "dac": int,
        "fi": int,
        "sub_id": int,
        "voltage": int,
        "spare": int,
        "req_dac": int,
        "spare2": int,
        "spare3": int,
        "spare4": int,
    },

    '7' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "acks": list,
    },


    '8' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "spare": int,
        "dac": int,
        "fi": int,
        "eu_id": str,
        "length": float,
        "beam": float,
        "ship_type": int,
        "haz_cargo": int,
        "draught": float,
        "loaded": int,
        "speed_qual": int,
        "course_qual": int,
        "heading_qual": int,
        "spare2": int,
        "x": float,
        "y": float,
        "position_accuracy": int,
        "utc_day": int,
        "utc_hour": int,
        "utc_min": int,
        "wind_ave": int,
        "wind_gust": int,
        "wind_dir": int,
        "wind_gust_dir": int,
        "air_temp": float,
        "rel_humid": int,
        "dew_point": float,
        "air_pres": float,
        "air_pres_trend": int,
        "horz_vis": float,
        "water_level": float,
        "water_level_trend": int,
        "surf_cur_speed": float,
        "surf_cur_dir": int,
        "cur_speed_2": float,
        "cur_dir_2": int,
        "cur_depth_2": int,
        "cur_speed_3": int,
        "cur_dir_3": int,
        "cur_depth_3": int,
        "wave_height": bool,
        "wave_period": int,
        "wave_dir": int,
        "swell_height": float,
        "swell_period": int,
        "swell_dir": int,
        "sea_state": int,
        "water_temp": float,
        "precip_type": int,
        "salinity": float,
        "ice":int,
    },

    '9' : {
        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "alt": int,
        "sog": float,
        "position_accuracy": int,
        "x": float,
        "y": float,
        "cog": float,
        "dte": int,
        "raim": bool,
        "assigned_mode": int,
        "timestamp": int,
        "alt_sensor": int,
        "spare": int,
        "sync_state": int,
        "slot_timeout": int,
        "slot_number": int,
        "spare2": int,
    },

    '10' : {
        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "dest_mmsi": int,
        "spare2": int,
        "spare": int
    },

    '11' : {
        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "year": int,
        "month": int,
        "day": int,
        "hour": int,
        "minute": int,
        "second": int,
        "position_accuracy": int,
        "x": float,
        "y": float,
        "fix_type": int,
        "transmission_ctl": int,
        "spare": int,
        "raim": bool,
        "sync_state": int,
        "slot_timeout": int,
        "slot_offset": int,

    },

    '12' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "seq_num": int,
        "dest_mmsi": int,
        "retransmitted": bool,
        "text": str,
        "spare": int
    },

    '13' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "mmsi_1": int,
    },

    '14' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "spare": int,
        "spare2": int,
        "text": str,
    },

    '15' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "spare": int,
        "mmsi_1": int,
        "msg_1_1": int,
        "slot_offset_1_1": int,
        "spare2": int,
        "dest_msg_1_2": int,
        "slot_offset_1_2": int,
        "spare3": int,
        "mmsi_2": int,
        "msg_2": int,
        "slot_offset_2": int,
        "spare4": int,
    },

    '16' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "spare": int,
        "dest_mmsi_a": int,
        "offset_a": int,
        "inc_a": int,
        "dest_mmsi_b": int,
        "offset_b": int,
        "inc_b": int,
        "spare2": int
    },

    '17' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "x": float,
        "y": float,
        "spare": int,
        "spare2": int
    },

    '18' : {

        "id": int,
        "mmsi": int,
        "repeat_indicator": int,
        "sog": float,
        "spare": int,
        "position_accuracy": int,
        "cog": float,
        "true_heading": int,
        "x": float,
        "y": float,
        "timestamp": int,
        "spare2": int,
        "unit_flag": int,
        "display_flag": int,
        "dsc_flag": int,
        "band_flag": int,
        "m22_flag": int,
        "mode_flag": int,
        "raim": bool,
        "commstate_flag": int,
        "commstate_cs_fill": int
    },

    '19' : {

        "id": int,
        "mmsi": int,
        "repeat_indicator": int,
        "sog": float,
        "spare": int,
        "position_accuracy": int,
        "x": float,
        "y": float,
        "cog": float,
        "true_heading": int,
        "time_stamp": int,
        "spare2": int,
        "name": str,
        "type_and_cargo": int,
        "dim_a": int,
        "dim_b": int,
        "dim_c": int,
        "dim_d": int,
        "fix_type": int,
        "raim": bool,
        "dte": int,
        "assigned_mode": int,
        "spare3": int,
        "timestamp": int,
    },

    '20' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "spare": int,
        "reservations": list,

    },

    '21' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "aton_type": int,
        "name": str,
        "position_accuracy": int,
        "x": float,
        "y": float,
        "dim_a": int,
        "dim_b": int,
        "dim_c": int,
        "dim_d": int,
        "fix_type": int,
        "timestamp": int,
        "off_pos": bool,
        "aton_status": int,
        "raim": bool,
        "virtual_aton": bool,
        "assigned_mode": bool,
        "spare": int,
        "spare2": int,
    },

    '22' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "chan_a": int,
        "chan_b": int,
        "txrx_mode": int,
        "power_low": int,
        "addressed": bool,
        "x1": float,
        "y1": float,
        "x2": float,
        "y2": float,
        "chan_a_bandwidth": int,
        "chan_b_bandwidth": int,
        "zone_size": int,
        "spare2": int,
        "spare": int
    },

    '23' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "spare": int,
        "x": float,
        "y": float,
        "station_type": int,
        "type_and_cargo": int,
        "spare_2": int,
        "txrx_mode": int,
        "interval_raw": int,
        "quiet": int,
        "spare3": int,
    },

    '24' : {

        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "part_num": int,
        "name": str,
        "type_and_cargo": int,
        "vendor_id": str,
        "callsign": str,
        "dim_a": int,
        "dim_b": int,
        "dim_c": int,
        "dim_d": int,
        "spare": int,


    },

    '25' : {
        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "addressed": bool,
        "dest_mmsi_valid": bool,
        "dest_mmsi": int,
        "dac": int,
        "fi": int,
    },

    '26' : {
        "id": int,
        "repeat_indicator": int,
        "mmsi": int,
        "use_app_id": bool,
        "dest_mmsi_valid": bool,
        "dest_mmsi": int,
        "dac": int,
        "fi": int,
        "commstate_flag": int,
        "sync_state": int,
        "slot_timeout_valid": bool,
        "slot_timeout": int,
        "received_stations_valid": bool,
        "received_stations": int,
        "slot_number_valid": bool,
        "slot_number": int,
        "utc_valid": bool,
        "utc_hour": int,
        "utc_min": int,
        "utc_spare": int,
        "slot_offset_valid": bool,
        "slot_offset": int,
        "slot_increment_valid": bool,
        "slot_increment": int,
        "slots_to_allocate_valid": bool,
        "slots_to_allocate": int,
        "keep_flag_valid": bool,
        "keep_flag": bool,
    },

    '27' : {
            "id": int,
            "repeat_indicator": int,
            "mmsi": int,
            "position_accuracy": int,
            "raim": bool,
            "nav_status": int,
            "x": float,
            "y": float,
            "cog": float,
            "sog": float,
            "gnss": bool,
            "spare": int,
            },

}