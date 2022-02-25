import ais

def decode_ais(line):
    """
    Finds the AIS portion of the TCP data and decodes to a dictionary
    :param line: ais message string
    :return: dictionary of decoded AIS data
    """

    decoded = None
    # ignore g tags, can't handle for now
    if "g:" not in line:
        parts = line.split(",")
        try:
            decoded = ais.decode(parts[6], 0)
        except IndexError:
            pass
        except ais.DecodeError:
            pass

        return decoded


def extract_epoch(s):
    epoch_time = ''
    clean_time = s.replace("\\", "")
    c0 = clean_time.replace("!AIVDM", "")
    c = c0.replace("b'", "")
    c1 = c.replace("c:", "")
    c2 = c1[:10]
    for character in c2:
        if character.isnumeric():
            epoch_time += str(character)
    return epoch_time


