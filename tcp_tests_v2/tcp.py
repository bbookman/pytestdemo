import socket
import time
import datetime
from typing import Dict, Any
import backoff
import shared
import helpers
from loguru import logger
import sys
logger.add('logs/tcp.log', format='{time} {name} {message}', level='DEBUG',
           retention="10 days")
logger.level("VOLUME", no=18, color='<yellow>',  icon="🌍")


class Tools(object):

    """
    These are set from the Test object.  Test object passes these when it needs a connection:
    ===============================================================
    server: TCP server endpoint such as streamingv2.ais.spire.com
    port: TCP server port
    token: Auth token
    max_lines: maximum messages to process
    ===============================================================
    For internal use
    ===============================================================
    sock: internal use, do not set
    """

    def __init__(self,
                 server,
                 port,
                 token,
                 max_lines, ):
        self.server = server
        self.port = port
        self.token = token
        self.sock = False
        self.max_lines = max_lines

    def _setup_sock(self):
        """
        Initialize socket
        :return: None
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(90)
            self.sock.connect((self.server, self.port))
        except socket.error as e:
            logger.critical(f'CONNECTION FAILED: {e}')
        logger.debug("SOCK SET UP")

    @backoff.on_exception(
        backoff.expo,
        OSError,
        max_time=900,
        max_tries=20
    )
    def connect(self):
        """
        Send auth token
        """
        self._setup_sock()
        login = 'A|T|' + self.token + '|' + '\n'
        logger.debug(f'TRYING: {self.server}:{self.port} {login}')
        e = self.sock.sendall(login.encode('ASCII'))
        connected = not bool(e)
        if not connected:
            raise('CONNECTION ERROR')
        else:
            logger.debug('CONNECTED', level='DEBUG')


    def reset_checkpoint(self, reset_string=None):
        """
        DEPRICATED - I'M NOT CONVINCED THIS WORKS
        NOR DO I FULLY GET HOW TO FIX IT

        Reset checkpoint specified by reset_string
        Must be in format 2021-03-08T11:45:09.840Z
        """
        self._setup_sock()
        login = 'A|T|' + self.token + '|' + f'{reset_string}' + '\n'
        logger.debug(f'TRYING RESET: {self.server}:{self.port} {login}')
        self.sock.sendall(login.encode('ASCII'))
        logger.debug('RESET COMPLETE', level='DEBUG')
        self.sock.close()

    def read(self):
        """
        Gets stream data
        """
        try:
            received = self.sock.recv(4096)
            if received:
                return received
        except socket.timeout as e:
            logger.debug(e)
            sys.exit()

    def get_lines(self):
        """
        Gets a message
        """
        temp_buffer = self.read()
        buffering = False
        if not temp_buffer:
            logger.warning('BUFFER YIELDED NO DATA')
            yield "NO"
        else:
            buffering = True
            temp_buffer = temp_buffer.decode()

        while buffering:
            if "\n" in temp_buffer:
                (line, temp_buffer) = temp_buffer.split("\n", 1)
                if shared.line_count % 50000 == 0 and shared.line_count > 0:
                    logger.log("VOLUME", f'LINE_COUNT {shared.line_count} : {time.strftime("%H:%M:%S")}')
                yield line + "\n"
            else:
                more = self.read()
                more = more.decode()
                buffering = bool(more)
                if not more:
                    break
                else:
                    temp_buffer += more
        if temp_buffer:
            yield temp_buffer
        else:
            yield "NO"

    def start_processing(self):
        """
        Kicks off testing process, gets data
        Terminates if max_lines reached
        :return: message data dictionary
        """

        logger.debug(f'STARTED {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%m:%s")}')
        self.connect()
        reply = self.get_lines()
        results_dict = dict()
        for line in reply:
            if 'Keep-alive' in line:
                continue
            if line == "NO":
                logger.debug('NO LINE RECEIVED, SLEEPING 5')
                time.sleep(5)
                self.sock.close()
                self.connect()
            elif shared.line_count >= self.max_lines:
                break
            elif line:
                shared.line_count += 1
                message_dict = self.build_dictionary(line)
                results_dict[f'{datetime.datetime.utcnow()}'] = message_dict
        return results_dict


    def build_dictionary(self, message):
        """
        Creates a dictionary by parsing message
        The dictionary is used for tests
        """
        columns = [
            'c_tag',
            's_tag',
            'epoch',
        ]
        columns += shared.all_ais_fields
        columns += [
            'message_time',
            'g_tag',
            'ais_header_channel',
        ]

        message_dict: Dict[Any, Any] = dict()
        for key in columns:
            message_dict.setdefault(key, "")

        contents = message.split(',')
        ais_message_raw = contents[(len(contents) - 2)]
        message_dict["ais_message_raw"] = ais_message_raw

        def fix_s(s):
            return s.replace("\\s:", "")

        # AIS message: (for example: AIVDM,1,1,,A,15MgK45P3@G?fl0E`JbR0OwT0@MS,0*4E)

        def fix_c(c):
            result = c.replace("c:", "")
            result = result.replace("\\!AIVDM", "")
            return result[:10]

        try:
            if "s:" in contents[0]:
                message_dict['s_tag'] = fix_s(contents[0])
            elif "s:" in contents[1]:
                message_dict['s_tag'] = fix_s(contents[1])
            elif "s:" in contents[2]:
                message_dict['s_tag'] = fix_s(contents[2])
            else:
                message_dict['s_tag'] = ""
        except IndexError as e:
            logger.critical(f"""
            MESSAGE CONTENTS: {contents}
            {e}
            """)

        # handle g tag

        if "g:" in contents[0]:
            message_dict['g_tag'] = contents[0]
        elif "g:" in contents[1]:
            message_dict['g_tag'] = contents[1]
        elif "g:" in contents[2]:
            message_dict['g_tag'] = contents[2]
        else:
            message_dict['g_tag'] = ""

        # split g_tag
        g_contents = message_dict['g_tag']
        if g_contents:
            x = g_contents.replace("\\g:", "")
            indicators = x.split('-')
            message_dict['g_msg_part'] = indicators[0]
            message_dict['g_total_parts'] = indicators[1]
            message_dict['g_uid'] = indicators[2]

        # handle c tag
        if "c:" in contents[0]:
            message_dict['c_tag'] = fix_c(contents[0])
            epoch = helpers.extract_epoch(message_dict['c_tag'])
            message_dict['epoch'] = epoch
            message_dict['message_time'] = self.handle_time(epoch)
        elif "c:" in contents[1]:
            message_dict['c_tag'] = fix_c(contents[1])
            epoch = helpers.extract_epoch(message_dict['c_tag'])
            message_dict['epoch'] = epoch
            message_dict['message_time'] = self.handle_time(epoch)
        elif "c:" in contents[2]:
            message_dict['c_tag'] = fix_c(contents[2])
            epoch = helpers.extract_epoch(message_dict['c_tag'])
            message_dict['epoch'] = epoch
            message_dict['message_time'] = self.handle_time(epoch)
        else:
            message_dict['c_tag'] = ""
            message_dict['epoch'] = ""
            message_dict['message_time'] = ""

        # handle ais_header_channel
        ais_header_channel = (contents[(len(contents) - 3)])
        message_dict["ais_header_channel"] = ais_header_channel

        decoded = helpers.decode_ais(message)  # skips g tag
        if decoded:
            for key, value in decoded.items():
                message_dict[key] = value
        logger.debug("RETURNING MESSAGE DICTIONARY")
        return message_dict

    def handle_time(self, stamp):
        """
        Converts stamp to datetime
        """
        if type(stamp) == str:
            result = datetime.datetime.fromtimestamp(int(stamp)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            result = stamp.strftime('%Y-%m-%d %H:%M:%S')

        return result
