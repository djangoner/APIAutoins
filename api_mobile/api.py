# import requests
import logging

import aiohttp

from .config import AUTOINS_API_URL, AUTOINS_HEADERS
from .utils import get_proxy, policy_serial_check, random_string

logging.basicConfig(level=logging.INFO)


async def osago_android_api(serial: str, policy: str) -> dict:
    serial_valid = policy_serial_check(serial)
    if not serial_valid:
        raise ValueError("Invalid policy serial!")

    data = {
        # "guid": "4287A7B39C99476690B73B138DC77D8C",
        "guid": random_string(length=32),
        "policyNumberKey": policy,
        "policySerialKey": serial_valid,  # Must be in Russian!
        "userId": None
    }

    proxy = get_proxy()
    logging.info(f"Sending request to autoria with proxy={proxy}, data={data}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    AUTOINS_API_URL, json=data, headers=AUTOINS_HEADERS, proxy=proxy) as resp:
                result = await resp.json()
                logging.info(f"Raw result: {result}")
                return result
    except Exception as e:
        logging.error(f"Request error: {e}")
        return False
    # else:
    #     return R.json()


# print(osago_android_api(serial="ХХХ", policy="0139038154"))
# print(osago_android_api(serial="ККК", policy="3000431308"))
