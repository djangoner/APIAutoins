import os
from api_mobile.config import PROXYS_FILE, WORKING_POLICIES_FILE
from random import choice

POLICY_SERIALS = {
    "KKK": "ККК",
    "MMM": "МММ",
    "EEE": "ЕЕЕ",
    "XXX": "ХХХ",
    "AAC": "ААС",
    "AAB": "ААВ",
    "TTT": "ТТТ",
    "PPP": "РРР",
    "HHH": "ННН",
}

PROXYS = []
WORKING_POLICIES = []


def read_proxys_file() -> None:
    """ Read proxys file. Line format: http://user:pass@some.proxy.com """

    PROXYS.clear()
    if not os.path.exists(PROXYS_FILE):
        with open(PROXYS_FILE, "w", encoding="utf8") as f:
            f.write("")

    with open(PROXYS_FILE, "r", encoding="utf8") as f:
        for line in f.readlines():
            if not line:
                continue
            PROXYS.append(line)


def read_working_policies_file() -> None:
    """ Read proxys file. Line format: XXX:0123456789 """

    WORKING_POLICIES.clear()
    if not os.path.exists(WORKING_POLICIES_FILE):
        with open(WORKING_POLICIES_FILE, "w", encoding="utf8") as f:
            f.write("")

    with open(WORKING_POLICIES_FILE, "r", encoding="utf8") as f:
        for line in f.readlines():
            if not line:
                continue
            WORKING_POLICIES.append(line.split(":"))


def random_string(length=16):
    """ Generate a random string with specified length """
    ABC = "abcdefghijklmnopqrstuvwxyz".upper() + "1234567890"
    return "".join([choice(ABC) for i in range(length)])


def policy_serial_check(serial: str):
    """ Check policy serial """
    if serial in POLICY_SERIALS.keys():  # Can convert
        return POLICY_SERIALS[serial]
    elif serial in POLICY_SERIALS.values():  # Valid
        return serial
    else:
        return False


def get_proxy() -> str:
    """ Get a random proxy from list """
    if not PROXYS:
        read_proxys_file()

    if len(PROXYS) < 1:
        return None
    else:
        return choice(PROXYS)


def get_working_policy() -> str:
    """ Get a random working pilycy from list """
    if not WORKING_POLICIES:
        read_working_policies_file()

    if len(WORKING_POLICIES) < 1:
        return None
    else:
        return choice(WORKING_POLICIES)
