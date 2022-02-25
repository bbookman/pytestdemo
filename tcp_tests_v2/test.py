import jira
import tcp
from loguru import logger
from datetime import datetime, timedelta
from shapely.geometry import Point, Polygon
import re
import time
import sys
logger.add('logs/test_core.log', format='{time} {name} {message}', level='DEBUG',
           retention="10 days")
logger.level("FAIL", no=11, color="<red>", icon="⛈")

class Test(object):
    """
    server: TCP server endpoint such as streamingv2.ais.spire.com
    port: TCP server port
    token: Auth token
    max_lines: maximum number of lines to process
    polygon: Optional. used in AOI testing
    label: Optional. used for logging and Jira issue summary
    reset_string: Optional.  Used if checkpoint reset is desired.  Must be in format 2021-03-08T11:45:09.840Z
    """

    def __init__(self,
                 server,
                 port,
                 token,
                 max_lines=1,
                 polygon= '',
                 label='automated',
                 reset_string=''):
        self.jira = jira.JiraTools(label=label)
        self.server = server
        self.token = token
        self.port = port
        self.max_lines = max_lines
        self.polygon = polygon
        self.get_data = tcp.Tools(self.server, self.port, self.token, self.max_lines)
        self.label = label
        self.reset_string = reset_string


    def validate_message_types(self):
        """
        Parses the data stream for Type id.
        Test requires a good number of lines, set max lines to a few million.
        The reason is that some types are rare.  Each type, once found, is marked as passed, so
        setting max_lines high does not mean every single line will get processed.

        If the max_lines are processed and the type is not found, a jira ticket is filed as Fail
        When the type is found, a jira ticket is filed as Passed
        """
        for t in range(1,27):
            test_summary = f"CONTAINS MESSAGE TYPE {t} | {self.label}"
            data = self.get_data.start_processing()
            for timestamp_key, msg_dict in data.items():
                if msg_dict['id'] == t:
                    self.jira.new_issue(f'{test_summary}', status='Passed')
                    logger.success(f'PASSED: {test_summary}')
                    return
            info = f'MESSAGE TYPE NOT FOUND: {t}\n' + str([f'{k}:{v}' for k, v in msg_dict.items()])
            self.jira.new_issue(f"{test_summary}", description=info, status='Fail')
            logger.log("FAIL", test_summary + '\n' + info)


    def validate_epoch(self):
        """
        Parses the data stream for the c: tag
        Cleans the tag and checks if it is a valid epoch
        Checks all messages in max_lines, so decide what makes sense for the test purpose

        If any c: value is not an epoch, the test will fail and file a Failed Jira ticket
        """
        test_summary = f"VALIDATE EPOCH | {self.label}"
        data = self.get_data.start_processing()
        for timestamp in data:
            msg = data[timestamp]
            e = msg['epoch']
            msg_string = str([f'{k}:{v}\n' for k, v in msg.items()])
            if not str(e).isdigit() or not len(e) == 10:
                info = f"""
                EPOCH: {e}
                MESSAGE: 
                {msg_string}
                """
                self.jira.new_issue(f"{test_summary}", description=info, status='Fail')
                logger.log("FAIL", test_summary + '\n' + info)
                return
        self.jira.new_issue(f'{test_summary}', status='Passed')
        logger.success(f'PASSED: {test_summary}')


    def validate_terrestrial(self):
        """
        At least one message will contain a c: tag with value = 'terrestrial'
        Once one is found, a Jira ticket is filed as Passed
        If none are found in the messages of max_lines, a Jira ticket is filed as Failed
        """
        test_summary = f"VALIDATE TERRESTRIAL SOURCE TAG | {self.label}"
        data = self.get_data.start_processing()
        info = ''
        for timestamp in data:
            msg = data[timestamp]
            t = msg['s_tag']
            tag = t.replace("\\", "")
            s_tag = tag.replace("s:", "")
            info = f"""
            s_tag: {s_tag}
            'terrestrial' in s_tag: {'terrestrial' in s_tag}
            s_tag is alpha: {s_tag.isalpha()}
            s_tag length <= 11: {len(s_tag) <= 11}
            """
            if 'terrestrial' in s_tag and s_tag.isalpha() and len(s_tag) <= 11:
                logger.success(f'PASSED: {test_summary}')
                self.jira.new_issue(f'{test_summary}', description=info, status='Passed')
                return
        self.jira.new_issue(f"{test_summary}", description=info,status='Fail')
        logger.log("FAIL", test_summary + '\n' + info)


    def validate_no_terrestrial(self):
        """
        No messages in max_lines c: tag with value = 'terrestrial'
        If one is found in the messages of max_lines, a Jira ticket is filed as Failed
        If none are found, Jira ticket is filed as Passed
        """

        test_summary = f"VALIDATE NO TERRESTRIAL | {self.label}"
        data = self.get_data.start_processing()
        for timestamp in data:
            msg = data[timestamp]
            t = msg['s_tag']
            tag = t.replace("\\", "")
            s_tag = tag.replace("s:", "")
            info = f"""
                        s_tag: {s_tag}
                        'terrestrial' in s_tag: {'terrestrial' in s_tag}
                        s_tag is alpha: {s_tag.isalpha()}
                        s_tag length <= 11: {len(s_tag) <= 11}
                        """
            if 'terrestrial' in s_tag:
                self.jira.new_issue(f"{test_summary}", description=info, status='Fail')
                logger.log("FAIL", test_summary + '\n' + info)
                return
        self.jira.new_issue(f'{test_summary}', description=info, status='Passed')
        logger.success(f'PASSED: {test_summary}')


    def validate_dynamic(self):
        """
        At least one message contains c: tag 'dynamic'
        If a single message is found with 'dynamic' the test passes and Jira ticket is filed
        If no messages in max_lines is 'dynamic' a Jira ticket is filed as Fail
        """
        test_summary = f"VALIDATE DYNAMIC SOURCE TAG | {self.label}"
        data = self.get_data.start_processing()
        for timestamp in data:
            msg = data[timestamp]
            t = msg['s_tag']
            tag = t.replace("\\", "")
            s_tag = tag.replace("s:", "")
            if 'dynamic' in s_tag and s_tag.isalpha() and len(s_tag) <= 7:
                self.jira.new_issue(f'{test_summary}', status='Passed')
                logger.success(f'PASSED: {test_summary}')
                return
        info = f"""
        last s_tag: {s_tag}
        'DYNAMIC' in s_tag: {'dynamic' in s_tag}
        s_tag is alpha: {s_tag.isalpha()}
        s_tag length <=7: {len(s_tag) <= 7}
        """
        self.jira.new_issue(f"{test_summary}", description=info,status='Fail')
        logger.log("FAIL", test_summary + '\n' + info)


    def validate_no_dynamic(self):
        """
        No messages contain c: tag 'dynamic'
        If a single message is found with 'dynamic' a Jira ticket is filed as Fail
        Otherwise Jira ticket is filed as Passed
        """
        test_summary = f"VALIDATE NO DYNAMIC SOURCE TAG | {self.label}"
        data = self.get_data.start_processing()
        for timestamp in data:
            msg = data[timestamp]
            t = msg['s_tag']
            tag = t.replace("\\", "")
            s_tag = tag.replace("s:", "")
            if 'dynamic' in s_tag:
                self.jira.new_issue(f"{test_summary}", description=s_tag, status='Fail')
                logger.log("FAIL", test_summary + '\n' + s_tag)
        self.jira.new_issue(f'{test_summary}', status='Passed')
        logger.success(f'PASSED: {test_summary}')


    def validate_norad_id(self):
        """
        Checks s: tag for Norad id.  If at least one is found, Jira ticket is filed as Passed
        If no Norad id are found in max_lines, Jira ticket is filed as Fail
        """
        test_summary = f"VALIDATE NORAD ID | {self.label}"
        data = self.get_data.start_processing()
        info = 'no s_tags found'
        for timestamp in data:
            msg = data[timestamp]
            t = msg['s_tag']
            tag = t.replace("\\", "")
            s_tag = tag.replace("s:", "")
            if 'terrestrial' in s_tag or 'dynamic' in s_tag:
                continue
            elif s_tag.isdigit() and len(s_tag) == 5 and "FM" not in s_tag:
                self.jira.new_issue(f'{test_summary}', status='Passed')
                logger.success(f'PASSED: {test_summary}')
                return
            else:
                info = f"""
                s_tag: {s_tag}
                s_tag is digit: {s_tag.isdigit()}
                s_tag length of 5: {len(s_tag) == 5}
                s_tag no 'FM': {"FM" not in s_tag}
                """
        self.jira.new_issue(f"{test_summary}", description=info, status='Fail')
        logger.log("FAIL", test_summary + '\n' + info)

    def validate_no_norad_id(self):
        """
        If no norad id is found in max_lines, Jira ticket is filed as Pass
        If a single norad id is found, Jira ticket is filed as Fail
        """
        test_summary = f"VALIDATE NO NORAD ID | {self.label}"
        data = self.get_data.start_processing()
        for timestamp in data:
            msg = data[timestamp]
            t = msg['s_tag']
            tag = t.replace("\\", "")
            s_tag = tag.replace("s:", "")
            no_fm = s_tag.replace('FM', '')
            info = f"""
                                  s_tag: {s_tag}
                                  s_tag is digit: {s_tag.isdigit()}
                                  s_tag length of 5: {len(s_tag) == 5}
                                  """
            if len(no_fm) == 5:
                self.jira.new_issue(f"{test_summary}", description=info, status='Fail')
                logger.log("FAIL", test_summary + '\n' + info)
                return
        self.jira.new_issue(f'{test_summary}', status='Passed')
        logger.success(f'PASSED: {test_summary}')


    def validate_spire_id(self):
        """
        If a single instance of s: tag containing a spire sat id is found, Jira ticket filed as Passed
        If no message in max_lines has spire sat id, Jira ticket is filed as Fail
        """
        test_summary = f"VALIDATE SPIRE ID | {self.label}"
        data = self.get_data.start_processing()
        info = ''
        for timestamp in data:
            msg = data[timestamp]
            t = msg['s_tag']
            tag = t.replace("\\", "")
            s_tag = tag.replace("s:", "")
            info = f"""
               last s_tag: {s_tag}
               'FM' in s_tag: {'FM' in s_tag}
               s_tag length <= 5: {len(s_tag) <= 5}
               """
            if 'terrestrial' in s_tag or 'dynamic' in s_tag:
                continue
            elif "FM" in s_tag and len(s_tag) <= 5:
                self.jira.new_issue(f'{test_summary}', info, status='Passed')
                logger.success(f'PASSED: {test_summary}')
                return
            else:
                continue
        self.jira.new_issue(f'{test_summary}', info, status='Fail')
        logger.log("FAIL", test_summary + '\n' + info)

    def validate_no_spire_id(self):
        """
        If a single s: tag contains a spire sat id, a Jira ticket is filed as Fail
        If no max_lines messages contain spire id, Jira ticket is filed as Passed
        """
        test_summary = f"VALIDATE SPIRE ID | {self.label}"
        data = self.get_data.start_processing()
        for timestamp in data:
            msg = data[timestamp]
            info = msg['s_tag']
            if 'terrestrial' in info or 'dynamic' in info:
                continue
            if 'FM' in info:
                self.jira.new_issue(f"{test_summary}", description=info, status='Fail')
                logger.log("FAIL", test_summary + '\n' + info)
                return
        self.jira.new_issue(f'{test_summary}', status='Passed')
        logger.success(f'PASSED: {test_summary}')


    def validate_aoi(self):
        """
        If a single message is found to be outside the polygon, Jira ticket is filed as Fail
        If all messages in max_lines are within polygon, Jira ticket is Passed
        """
        test_summary = f"VALIDATE AOI {self.label}"
        data = self.get_data.start_processing()

        for timestamp in data:
            msg = data[timestamp]
            if msg['x']:
                p1 = msg['x']
            else:
                continue
            if msg['y']:
                p2 = msg['y']
            else:
                continue
            # Create a Polygon
            nums = re.findall(r'\d+(?:\.\d*)?', self.polygon.rpartition(',')[0])
            coords = zip(*[iter(nums)] * 2)
            poly = Polygon(coords)
            info = f"""
            EXPECTED: {self.polygon}
            RESULT:   {p1},{p2}
            """
            if p1.within(poly) and p2.within(poly):
                continue
            else:
                self.jira.new_issue(f'{test_summary}', description=info, status='Fail')
                logger.log("FAIL", test_summary + '\n' + info)
                return
        self.jira.new_issue(f'{test_summary}', status='Passed')
        logger.success(f'PASSED: {test_summary}')



    def validate_ais_required_fields(self):
        """
        If any message is found to be missing id (type), mmsi or repeat_indicator, Jira ticket filed as Fail
        If all max_lines contain the required fields, Jira ticket filed as Passed
        """
        test_summary = f"VALIDATE DEFAULT AIS FIELDS | {self.label}"
        data = self.get_data.start_processing()
        for timestamp in data:
            msg = data[timestamp]
            if msg['g_tag']:  # skip g tags for now TODO
                return
            msg_id = str(msg['id'])
            mmsi = str(msg['mmsi'])
            ri = msg['repeat_indicator']
            msg_dcode = ''
            for k, v in msg.items():
                msg_dcode+=f"{k}:{v}\n"

            info = f"""
                         TYPE: {msg_id}
                         MMSI: {mmsi}
                         REPEAT INDICATOR: {ri}
                         RAW AIS: {msg["ais_message_raw"]}
                         AIS DECODE:
                         {msg_dcode}
                         """

            if not msg_id.isdigit() or not mmsi.isdigit() or len(mmsi) < 9 or not int(ri) <= 3:
                self.jira.new_issue(f"{test_summary}", description=info, status='Fail')
                logger.log("FAIL", test_summary + '\n' + info)
                return
        self.jira.new_issue(f'{test_summary}', status='Passed')
        logger.success(f'PASSED: {test_summary}')

    def validate_no_g_tags(self):
        """
        If any message contains a g tag, Jira ticket filed as Fail
        If no messages in max_lines contain g tag, Jira ticket filed as Passed
        """
        test_summary = f"VALIDATE NO G TAG PRESENT | {self.label}"
        data = self.get_data.start_processing()
        for timestamp in data:
            msg = data[timestamp]
            info = [f'{k},{v}' for k, v in timestamp.items()]
            if msg['g_tag']:
                self.jira.new_issue(f"{test_summary}", description=info, status='Fail')
                logger.log("FAIL", test_summary + '\n' + info)
                return
        self.jira.new_issue(f'{test_summary}', status='Passed')
        logger.success(f'PASSED: {test_summary}')

    def measure_catch_up_time(self):
        """
        DEPRECATED - not sure this works
        self.reset_string format 2021-03-08T11:45:09.840Z
        """
        info = ''
        start_catch_up = datetime.utcnow()
        t = tcp.Tools(server=self.server, port=self.port, token=self.token, max_lines=1)
        # reset appears not to work, try manual
        #t.reset_checkpoint(self.reset_string)
        t.connect()
        first_epoch = ''

        def epoch_is_now(message_epoch):
            now = datetime.utcnow()
            five_seconds_ago = timedelta(seconds=-5)
            five_seconds_from_now = timedelta(seconds=+5)
            current_epoch = datetime.fromtimestamp(int(message_epoch))
            yes = now + five_seconds_ago <= current_epoch <= now+five_seconds_from_now
            difference = now - start_catch_up
            i = f"""
                    STARTED CATCH UP: {t.handle_time(start_catch_up)}
                    FIRST EPOCH:      {t.handle_time(first_epoch)} 
                    CURRENT EPOCH:    {t.handle_time(current_epoch )}
                    LAST EPOCH:       {t.handle_time(message_epoch)}
                    FINISHED AT:      {t.handle_time(now)}
                    DIFFERENCE:       {difference}
                                          """
            if yes:
                logger.log("VOLUME", i)
                return True
            return False

        while True:
            reply = t.get_lines()
            for line in reply:
                if 'Keep-alive' in line:
                    continue
                elif line == "NO":
                    logger.debug('NO LINE RECEIVED, SLEEPING 5')
                    time.sleep(5)
                    self.sock.close()
                    self.connect()
                    continue
                elif 'g:' in line:
                    continue
                else:
                    split_line = line.split(',')
                    try:
                        c_tag = split_line[1]
                    except IndexError as e:
                        logger.error(e)
                        break
                    if 'c:' in c_tag:
                        c_loc = c_tag.find('c:')
                        epoch = c_tag[c_loc+2:-10]
                        if not first_epoch:
                            first_epoch = epoch
                            info += f"""
                            START:       {t.handle_time(start_catch_up)}
                            FIRST EPOCH: {t.handle_time(first_epoch)}
                            """
                            logger.info(info)
                        if epoch_is_now(epoch):
                            sys.exit(0)

    def minutes_per_line(self):
        """
        DEPRICATED, not sure this works
        """
        self.get_data.reset_checkpoint(self.reset_string)
        start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        data = True
        while data:
            data = self.get_data.start_processing()
        end_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        logger.log("VOLUME", f"""
        !!!! DONE !!!!!
        START: {start_time}
        END  : {end_time}
        TOTAL LINES: {len(data)}
        """)

    def save_data_local(self):
        """
        Saves data to local file
        """
        data = self.get_data.start_processing()
        if data:
            for message in data:
                with open('data.csv', 'a+') as f:
                    f.write(message)
        else:
            logger.critical("NO DATA, EXITING")








