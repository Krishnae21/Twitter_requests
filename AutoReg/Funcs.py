import json
import string
import random

import requests
from twocaptcha import TwoCaptcha


def get_random_string(len):
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(len)
    )


def parseArkose(text: str):
    do = 'arkose_challenge_signup_web_prod":{"value":"'
    txt = text[text.find(do) + len(do) :]
    txt = txt[: txt.find('"')]
    return txt


def parseGt(text: str):
    gt_pos = text.find("""cookie="gt=""")
    gt = None
    if gt_pos != -1:
        gt = text[gt_pos + 11 : gt_pos + 11 + 19]
    return gt


def getArkoseAnswer(arkose: str):
    config = {
        "server": "2captcha.com",
        "apiKey": "2608d882d4fc7b1e6b4c9cc84d1746e5",
        "softId": 123,
        "defaultTimeout": 220,
        "pollingInterval": 5,
    }
    solver = TwoCaptcha(**config)

    try:
        result = solver.funcaptcha(
            sitekey=arkose,
            url="https://twitter.com",
            surl="https://client-api.arkoselabs.com",
            # proxy={
            #     "type": "Socks5",
            #     "uri": "4091212-corporate-country-NL:1hcwlb7svw@93.190.138.107:12145",
            # }
            #     http://4015448-res-country-GB:5owkallqs@93.190.142.139:12801
        )
        if result != None:
            return result.get("code")
        return result

    except Exception as e:
        print(e)
#
# print(getArkoseAnswer('2CB16598-CB82-4CF7-B332-5990DB66F3AB'))

# flow = "flowtest"
# flow = flow[0:-1]
# flow = flow + "3"
# print(flow)