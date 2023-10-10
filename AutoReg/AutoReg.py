import json
import random
from http.cookiejar import Cookie

import requests
from requests.cookies import RequestsCookieJar
from Data import onboarding_headers
import Data
import Funcs


class Requests:
    session = requests.session()
    proxy = {"https": "127.0.0.1:8080", "http": "127.0.0.1:8080"}
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    ua = {"User-Agent": user_agent}
    headers = {**Data.onboarding_headers, "User-Agent": user_agent}
    data = {"csrf": Funcs.get_random_string(32)}

    def getFirstData(self):
        try:
            response = self.session.get(
                "https://twitter.com/",
                headers=self.ua,
                verify=False,
                proxies=self.proxy,
            )

            arkose = Funcs.parseArkose(response.text)
            gt = Funcs.parseGt(response.text)
            self.data.update({"Arkose": arkose, "gt": gt})
            gt_cook = requests.cookies.create_cookie(
                name="gt", value=self.data.get("gt")
            )
            self.session.cookies.set_cookie(gt_cook)
            return True
        except requests.exceptions.RequestException as e:
            return False

    def getFlowToken(self):
        self.headers["X-Guest-Token"] = self.data.get("gt")
        self.headers["X-Csrf-Token"] = self.data.get("csrf")
        self.headers.update(onboarding_headers)
        self.session.cookies.set_cookie(
            requests.cookies.create_cookie("ct0", self.data.get("csrf"))
        )

        url: str = "https://api.twitter.com/1.1/onboarding/task.json?flow_name=signup"

        response = self.session.post(
            url,
            json=Data.onboarding_signup_json,
            headers=self.headers,
            proxies=self.proxy,
            verify=False,
        )
        if response.status_code == 200:
            self.data["flow"] = json.loads(response.text).get("flow_token")



    def checkEmail(self, email: str) -> bool:
        response = self.session.get(
            f"https://twitter.com/i/api/i/users/email_available.json?email={email}",
            headers=self.headers,
            proxies=self.proxy,
            verify=False,
        )
        if response.text.find('valid":true') != -1:
            return True
        return False

    def emailVerif(self) -> bool:
        data = {
            "email": self.data.get("email"),
            "display_name": self.data.get("username"),
            "flow_token": self.data.get("flow"),
        }
        response = self.session.post(
            "https://api.twitter.com/1.1/onboarding/begin_verification.json",
            json=data,
            proxies=self.proxy,
            verify=False,
            headers=self.headers,
        )
        if response.status_code == 204:
            self.data["email_code"] = input("Email code: ")
            return True
        return False

    def registerEnd(self):
        birthday = self.data.get("birth_date")
        data = {
            "flow_token": self.data.get("flow"),
            "subtask_inputs": [
                {
                    "subtask_id": "Signup",
                    "sign_up": {
                        "link": "email_next_link",
                        "name": self.data.get("username"),
                        "email": self.data.get("email"),
                        "birthday": {"day": birthday[0], "month": birthday[1], "year": birthday[2]},
                        "personalization_settings": {
                            "allow_cookie_use": True,
                            "allow_device_personalization": True,
                            "allow_partnerships": True,
                            "allow_ads_personalization": True,
                        },
                    },
                },
                {
                    "subtask_id": "SignupSettingsListEmail",
                    "settings_list": {
                        "setting_responses": [
                            {
                                "key": "twitter_for_web",
                                "response_data": {"boolean_data": {"result": True}},
                            }
                        ],
                        "link": "next_link",
                    },
                },
                {
                    "subtask_id": "SignupReview",
                    "sign_up_review": {"link": "signup_with_email_next_link"},
                },
                {
                    "subtask_id": "ArkoseEmail",
                    "web_modal": {
                        "completion_deeplink": f"""twitter://onboarding/web_modal/next_link?access_token={self.data.get("arkose_answer")}""",
                        "link": "signup_with_email_next_link",
                    },
                },
                {
                    "subtask_id": "EmailVerification",
                    "email_verification": {
                        "code": self.data.get("email_code"),
                        "email": self.data.get("email"),
                        "link": "next_link",
                    },
                },
            ],
        }
        response = self.session.post(
            Data.task_url,
            headers=self.headers,
            json=data,
            proxies=self.proxy,
            verify=False,
        )
        if response.status_code == 200:
            flow = json.loads(response.text).get("flow_token")
            self.data.update({"flow": flow})
            return True
        return False

    def sendPassword(self):
        self.data.update({"csrf": Funcs.get_random_string(32)})
        self.headers["X-Csrf-Token"] = self.data.get("csrf")
        self.headers["X-Client-Transaction-Id"] = "Sr5skttNNtTx2RBagADepfaihT4EBgOhEetJ2unL7jWYOyglXclamD0sPUcVkdpy+rUs8UrVLV8UY2zbCKUeCQwl1zYjxw"
        self.session.cookies.set("ct0", self.data.get("csrf"))

        flow = self.data.get("flow")
        data = {
            "flow_token": flow,
            "subtask_inputs": [
                {
                    "subtask_id": "EnterPassword",
                    "enter_password": {"password": "AXsusa54h", "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            Data.task_url,
            headers=self.headers,
            json=data,
            proxies=self.proxy,
            verify=False,
        )
        if response.status_code == 200:
            print("good")
            for cookie in response.cookies:
                print(cookie)

    def passwordStrendth(self):
        data = {"password": "Ideapads340", "username": self.data.get("username")}
        response = self.session.post("https://api.twitter.com/1.1/account/password_strength.json", data=data, headers=self.headers, proxies=self.proxy, verify=False)
        if response.status_code == 200:
            return True
        return False

if __name__ == "__main__":
    email = input("Email: ")
    req = Requests()
    req.data["email"] = email
    req.data["username"] = Funcs.get_random_string(10)
    req.data["birth_date"] = [random.randint(1, 20), random.randint(1, 12), random.randint(1990, 2000)]
    cookies = req.getFirstData()
    req.getFlowToken()

    if req.checkEmail(email) & req.emailVerif():
        # req.data["arkose_answer"] = Funcs.getArkoseAnswer(req.data.get("Arkose")) vasili.ew.vo.v1998@gmail.com
        req.data["arkose_answer"] = "7921788cf03abae97.4633839404|r=ap-southeast-1|meta=3|meta_width=558|meta_height=523|metabgclr=transparent|metaiconclr=%23555555|guitextcolor=%23000000|pk=2CB16598-CB82-4CF7-B332-5990DB66F3AB|pl=2|at=40|rid=92|ag=101|cdn_url=https%3A%2F%2Fclient-api.arkoselabs.com%2Fcdn%2Ffc|lurl=https%3A%2F%2Faudio-ap-southeast-1.arkoselabs.com|surl=https%3A%2F%2Fclient-api.arkoselabs.com|smurl=https%3A%2F%2Fclient-api.arkoselabs.com%2Fcdn%2Ffc%2Fassets%2Fstyle-manager"

        if req.data.get("arkose_answer") != None:
            print(req.data.get("arkose_answer"))
            if req.registerEnd():
                req.passwordStrendth()




                req.sendPassword()
        else:
            print("arkose_error")
    input("STOP")
