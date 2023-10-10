#! /bin/python

import json
import random
import re
import string
import time
import urllib.parse
from threading import Thread
from time import sleep, time_ns

import requests
from requests.api import request
from requests.sessions import session
from selenium import webdriver

proxy_X = {"http": "127.0.0.1:8080", "https": "127.0.0.1:8080"}


init_api_url = "https://twitter.com:443/i/api/1.1/branch/init.json"
onboarding_signup_url = (
    "https://twitter.com:443/i/api/1.1/onboarding/task.json?flow_name=signup"
)
onboarding_url = "https://twitter.com:443/i/api/1.1/onboarding/task.json"
check_email_url = "https://twitter.com:443/i/api/i/users/email_available.json?email={}"
client_events_url = "https://api.twitter.com:443/1.1/jot/client_event.json"
auth_bearer_js_url = (
    "https://abs.twimg.com:443/responsive-web/client-web/main.6c1aeb65.js"
)
twitter_sess_url = "https://twitter.com:443/i/js_inst?c_name=ui_metrics"
password_strength_url = (
    "https://twitter.com:443/i/api/1.1/account/password_strength.json"
)

twitter_sess_header = {
    "Connection": "close",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "script",
    "Referer": "https://twitter.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
client_event_headers_OPTIONS = {
    "Connection": "close",
    "Accept": "*/*",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "authorization,x-csrf-token,x-guest-token,x-twitter-active-user,x-twitter-client-language",
    "Origin": "https://twitter.com",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://twitter.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
client_event_headers_POST = {
    "Connection": "close",
    # "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "x-twitter-client-language": "en",
    # "x-csrf-token": "54b9d9e87a4fef1889d060be00437558",
    # "x-guest-token": "1321170979104632838",
    "x-twitter-active-user": "yes",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Origin": "https://twitter.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://twitter.com/",  # This entry will be changed later on
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
init_api_headers = {
    "Connection": "close",
    # "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "x-twitter-client-language": "en",
    # "x-csrf-token": "54b9d9e87a4fef1889d060be00437558",
    # "x-guest-token": "1321170979104632838",
    "x-twitter-active-user": "yes",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "content-type": "application/json",
    "Accept": "*/*",
    "Origin": "https://twitter.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://twitter.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
personalization_id_headers = {
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
auth_bearer_js_headers = {
    "Connection": "close",
    "Origin": "https://twitter.com",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "script",
    "Referer": "https://twitter.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
onboarding_headers = {
    "Connection": "close",
    # "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "X-twitter-client-language": "en",
    # "x-csrf-token": "54b9d9e87a4fef1889d060be00437558",
    # "x-guest-token": "1321170979104632838",
    "X-twitter-active-user": "yes",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "content-type": "application/json",
    "Accept": "*/*",
    "Origin": "https://twitter.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://twitter.com/i/flow/signup",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
optout_headers = {
    "Connection": "close",
    # "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "x-twitter-client-language": "en",
    # "x-csrf-token": "54b9d9e87a4fef1889d060be00437558",
    # "x-guest-token": "1321170979104632838",
    "x-twitter-active-user": "yes",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Origin": "https://twitter.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://twitter.com/i/flow/signup",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
check_email_header = {
    "Connection": "close",
    # "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "x-twitter-client-language": "en",
    # "x-csrf-token": "54b9d9e87a4fef1889d060be00437558",
    # "x-guest-token": "1321170979104632838",
    "x-twitter-active-user": "yes",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://twitter.com/i/flow/signup",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}


def time_ms():
    return time.time_ns() // 1000000


def get_random_string(len):
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(len)
    )


def get_random_number(len):
    return "".join(random.choice(string.digits) for _ in range(len))


# Add cookies: guest_id, personalization_id, gt, _twitter_sess
def get_twitter_cookies(session):
    personalization_id_url = "https://twitter.com:443/"
    response = session.get(
        personalization_id_url,
        headers=personalization_id_headers,
        proxies=proxy_X,
        verify=False,
    )  # guest_id, personalization_id
    if response is not None:
        response_gt = response.text
        print(response_gt)
    else:
        print("[!] Error downloading guest_id, personalization_id, gt cookies")
        return False
    gt_pos = response_gt.find("""cookie="gt=""")
    gt = None
    if gt_pos != -1:
        gt = response_gt[
            gt_pos + 11 : gt_pos + 11 + 19
        ]  # len(decodeURIComponent) = 23. len(gt) = 19
        cookie_obj = requests.cookies.create_cookie(
            domain=".twitter.com", path="/", name="gt", value=gt
        )  # gt
        session.cookies.set_cookie(cookie_obj)

    if gt is None:
        print("[!] Error downloading gt cookie")
        return False

    for cookie in session.cookies:
        if cookie.name not in [
            "guest_id",
            "personalization_id",
            "gt",
        ]:  # Cleanup cookies (no mobile ones)
            del session.cookies[cookie.name]

    # A random cookie
    ct0_cookie_obj = requests.cookies.create_cookie(
        domain=".twitter.com", path="/", name="ct0", value=get_random_string(32)
    )
    session.cookies.set_cookie(ct0_cookie_obj)

    return True


# Add to session all the random/fixed cookies which do not need requests
def generate_static_cookies(session):
    cookie_timestamp = str(int(time.time()))  # Used for _ga and _gid cookies
    cookie_ver = "GA1"
    cookie_subver = "2"  # WARNING check for updates in this cookie field for both _ga and _gid cookies

    # session.cookies["_ga"] = '.'.join( [cookie_ver, cookie_subver, get_random_number(9), cookie_timestamp] )
    ga_cookie = ".".join(
        [cookie_ver, cookie_subver, get_random_number(9), cookie_timestamp]
    )
    ga_cookie_obj = requests.cookies.create_cookie(
        domain=".twitter.com", path="/", name="_ga", value=ga_cookie
    )
    session.cookies.set_cookie(ga_cookie_obj)

    gid_cookie = ".".join(
        [cookie_ver, cookie_subver, get_random_number(9), cookie_timestamp]
    )
    gid_cookie_obj = requests.cookies.create_cookie(
        domain=".twitter.com", path="/", name="_gid", value=gid_cookie
    )
    session.cookies.set_cookie(gid_cookie_obj)


# Set uniform User-Agent for every header
def configure_user_agent(user_agent):
    client_event_headers_POST["User-Agent"] = user_agent
    init_api_headers["User-Agent"] = user_agent
    onboarding_headers["User-Agent"] = user_agent
    optout_headers["User-Agent"] = user_agent
    check_email_header["User-Agent"] = user_agent
    client_event_headers_OPTIONS["User-Agent"] = user_agent
    personalization_id_headers["User-Agent"] = user_agent
    auth_bearer_js_headers["User-Agent"] = user_agent
    twitter_sess_header["User-Agent"] = user_agent


# Add authorization bearer, x-csrf-token, x-guest-token
def update_headers(session):
    response = requests.get(
        auth_bearer_js_url,
        headers=auth_bearer_js_headers,
        proxies=proxy_X,
        verify=False,
    )
    if response is not None:
        response_js = response.text
    else:
        print("[!] Error downloading 'Bearer' identifier")
        return False
    bearer_pos = response_js.find("Web-12") + 11
    bearer = response_js[bearer_pos : bearer_pos + 104]

    client_event_headers_POST["authorization"] = "Bearer {}".format(bearer)
    client_event_headers_POST["x-csrf-token"] = session.cookies["ct0"]
    client_event_headers_POST["x-guest-token"] = session.cookies["gt"]

    init_api_headers["authorization"] = "Bearer {}".format(bearer)
    init_api_headers["x-csrf-token"] = session.cookies["ct0"]
    init_api_headers["x-guest-token"] = session.cookies["gt"]

    onboarding_headers["Authorization"] = "Bearer {}".format(bearer)
    onboarding_headers["X-csrf-token"] = session.cookies["ct0"]
    onboarding_headers["X-Guest-Token"] = session.cookies["gt"]

    optout_headers["authorization"] = "Bearer {}".format(bearer)
    optout_headers["x-csrf-token"] = session.cookies["ct0"]
    optout_headers["x-guest-token"] = session.cookies["gt"]

    check_email_header["authorization"] = "Bearer {}".format(bearer)
    check_email_header["x-csrf-token"] = session.cookies["ct0"]
    check_email_header["x-guest-token"] = session.cookies["gt"]


# Generate twitter client event logs. Should not be called directly but only by send_twitter_client_event
# Supported event types: storePrepare, empty, heartbeat, client_network_request_event, client_event
def twitter_client_event_log(events, sequence):  # TODO description request
    twitter_client_events_client_app_id = "3033300"
    ret_sequence = sequence
    ret_events = []
    for event in events:
        event_type = event["type"]
        if event_type == "storePrepare":
            parameters = "category=perftown"
            ret_events.extend(
                [
                    {
                        "description": "rweb:init:storePrepare",
                        "product": "rweb",
                        "duration_ms": random.randint(15, 25),
                    },
                    {
                        "description": "rweb:ttft:perfSupported",
                        "product": "rweb",
                        "duration_ms": random.randint(1, 5),
                    },
                    {
                        "description": "rweb:ttft:connect",
                        "product": "rweb",
                        "duration_ms": random.randint(30, 70),
                    },
                    {
                        "description": "rweb:ttft:process",
                        "product": "rweb",
                        "duration_ms": random.randint(500, 1000),
                    },
                    {
                        "description": "rweb:ttft:response",
                        "product": "rweb",
                        "duration_ms": random.randint(1, 5),
                    },
                    {
                        "description": "rweb:ttft:interactivity",
                        "product": "rweb",
                        "duration_ms": random.randint(800, 1500),
                    },
                ]
            )
        # No changes to ret_sequence in this case
        elif event_type == "empty":
            return (
                ret_sequence,
                "",
            )  # They wanted an empty string, so we gave them an empty string
        # No changes to ret_sequence in this case
        elif event_type == "heartbeat":
            parameters = "category=perftown"
            ret_events.append(
                {"description": "rweb:heartbeat:health:false", "product": "rweb"}
            )
        # No changes to ret_sequence in this case
        elif (
            event_type == "client_network_request_event"
        ):  # Event paramteres: triggered_on, start_time_ms, uri_host_name, uri_path, request_body_size
            parameters = ""  # TODO check this
            ret_events.append(
                {
                    "_category_": "client_network_request_event",
                    "format_version": 2,
                    "triggered_on": event["triggered_on"],  # 1603806896071
                    "request": {
                        "uri_scheme": "https:",
                        "uri_host_name": event["uri_host_name"],  # "api.twitter.com"
                        "uri_path": event[
                            "uri_path"
                        ],  # "/1.1/account/personalization/sync_optout_settings.json"
                        "uri_query": "",
                        "http_method": "POST",
                        "http_status_code": 200,
                        "start_time_ms": event["start_time_ms"],  # 1603806895496
                        "request_details": {
                            "duration_ms": random.randint(300, 700),
                            "request_body_size": event["request_body_size"],  # 0
                        },
                    },
                    "common_header": {
                        "commonHeader": {
                            "clientHeader": {
                                "timestampMs": event["triggered_on"],  # 1603806896071
                                "timezoneOffsetMin": 60,
                            }
                        }
                    },
                    "network_measurements": {
                        "connection_type": "unknown",
                        "speed_class": "3g",
                        "download_mbps": 1.4,
                        "rtt_ms": 400,
                        "reduced_data_usage": False,
                    },
                    "event_type": "api:all",
                    "event_source": "rweb",
                    "client_app_id": twitter_client_events_client_app_id,
                }
            )
            ret_sequence += 1
        elif (
            event_type == "client_event"
        ):  # Event paramteres: triggered_on, event_namespace, [items], sequence_start_timestamp
            # if "element" in event: # If key "element" is present
            # 	event_namespace = {
            # 		"page": event["page"], # "onboarding"
            # 		"element": event["element"], # "view"
            # 		"action": event["action"], # "show"
            # 		"client": "m5"
            # 	}
            # else:
            # 	event_namespace = {
            # 		"page": event["page"], # "onboarding"
            # 		"action": event["action"], # "show"
            # 		"client": "m5"
            # 	}
            parameters = "debug=true"
            event_namespace = event["event_namespace"]
            event_namespace["client"] = "m5"
            new_dict = {
                "_category_": "client_event",
                "format_version": 2,
                "triggered_on": event["triggered_on"],  # 1603806894895
                "event_namespace": event_namespace,
                "client_event_sequence_start_timestamp": event[
                    "sequence_start_timestamp"
                ],  # 1603806886131
                "client_event_sequence_number": ret_sequence,
                "client_app_id": twitter_client_events_client_app_id,
            }
            if "items" in event:  # If key "items" is present
                new_dict["items"] = event["items"]
            ret_events.append(new_dict)
            ret_sequence += 1

    json_string = json.dumps(ret_events, separators=(",", ":"))  # Me no likey spaces
    ret_string = "{}&log={}".format(parameters, urllib.parse.quote(json_string))
    return (ret_sequence, ret_string)


# Send twitter client event logs with the appropriate request type
def send_twitter_client_event(session, events, sequence=None):
    if len(events) == 1 and events[0]["type"] == "empty":
        response = requests.options(
            client_events_url, headers=client_event_headers_OPTIONS
        )
        ret_sequence = sequence
    else:
        ret_sequence, data = twitter_client_event_log(events, sequence)
        response = session.post(
            client_events_url,
            headers=client_event_headers_POST,
            data=data,
            proxies=proxy_X,
            verify=False,
        )
    return (True, ret_sequence) if response else (False, ret_sequence)


def solve_js_challenge(js_chal, driver):
    functions = re.findall(r"function \w{20}", js_chal)

    internal_func_name = functions[1].split(" ")[1]

    func_body_begin = js_chal.find("function " + internal_func_name + "()")
    func_body_end = js_chal.find("};};")

    response_text_body = js_chal[func_body_begin + 33 : func_body_end + 2]

    return json.dumps(
        driver.execute_script(response_text_body), separators=(",", ":")
    ).replace('"', '\\"')


# Send heartbeats every 20 seconds. Must be started by a thread
def keepalive(session):
    while True:
        time.sleep(20)
        if G.kill:  # Check right before firing a new heartbeat
            G.kill = False
            return
        send_twitter_client_event(session, [{"type": "heartbeat"}])


def register_twitter(session):
    email_address, password = input("Input email address: "), "secure!password"
    username = email_address.split("@")[0]
    client_event_sequence = 0

    configure_user_agent(
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    )
    cookies_status = get_twitter_cookies(session)
    if not cookies_status:
        print("[!] Error downloading cookies")
        return 1
    update_headers(session)

    # client event NaN - OPTIONS
    success, client_event_sequence = send_twitter_client_event(
        session, [{"type": "empty"}], client_event_sequence
    )

    # client event NaN bis - StorePrepare
    success, client_event_sequence = send_twitter_client_event(
        session, [{"type": "storePrepare"}], client_event_sequence
    )

    # client event 0 - front: show
    sequence_start = time_ms()
    client_events = [
        {
            "type": "client_event",
            "triggered_on": sequence_start,
            "items": [],
            "event_namespace": {"page": "front", "action": "show"},
            "sequence_start_timestamp": sequence_start,
        }
    ]
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # Download javascript challenge + `_twitter_sess` cookie
    js_chal = session.get(
        twitter_sess_url, headers=twitter_sess_header, proxies=proxy_X, verify=False
    )

    # Add fixed cookies
    generate_static_cookies(session)

    # client event 1,2 - smartlock: prompt, smartlock: no credentials
    triggered_0 = sequence_start
    triggered_1 = triggered_0 + random.randrange(20, 100)
    client_events = [
        {
            "type": "client_event",
            "triggered_on": triggered_0,
            "event_namespace": {
                "page": "app",
                "component": "smartlock_prompt",
                "action": "impression",
            },
            "items": [],
            "sequence_start_timestamp": sequence_start,
        },
        {
            "type": "client_event",
            "triggered_on": triggered_1,
            "event_namespace": {
                "page": "app",
                "component": "smartlock_prompt",
                "element": "no_credentials",
                "action": "cancel",
            },
            "items": [],
            "sequence_start_timestamp": sequence_start,
        },
    ]
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # Static cookie appearing right here
    sl_cookie_obj = requests.cookies.create_cookie(
        domain=".twitter.com", path="/", name="_sl", value="1"
    )
    session.cookies.set_cookie(sl_cookie_obj)

    # Init registration flow
    session.post(
        init_api_url, headers=init_api_headers, json={}, proxies=proxy_X, verify=False
    )  # Ignore response

    # Update client_event header
    client_event_headers_POST["Referer"] = "https://twitter.com/i/flow/signup"

    # client event 3 - signup_callout
    triggered_3 = time_ms()
    client_events = [
        {
            "type": "client_event",
            "triggered_on": triggered_3,
            "event_namespace": {
                "page": "front",
                "section": "front",
                "component": "signup_callout",
                "element": "form",
                "action": "signup",
            },
            "sequence_start_timestamp": sequence_start,
        }
    ]
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # Begin onboarding
    onboarding_signup_json = {
        "input_flow_data": {
            "requested_variant": '{\\"signup_type\\":\\"phone_email\\"}",',
            "flow_context": {
                "debug_overrides": {},
                "start_location": {"location": "splash_screen"},
            },
        },
        "subtask_versions": {
            "action_list": 2,
            "alert_dialog": 1,
            "app_download_cta": 1,
            "check_logged_in_account": 1,
            "choice_selection": 3,
            "contacts_live_sync_permission_prompt": 0,
            "cta": 7,
            "email_verification": 2,
            "end_flow": 1,
            "enter_date": 1,
            "enter_email": 2,
            "enter_password": 5,
            "enter_phone": 2,
            "enter_recaptcha": 1,
            "enter_text": 5,
            "enter_username": 2,
            "generic_urt": 3,
            "in_app_notification": 1,
            "interest_picker": 3,
            "js_instrumentation": 1,
            "menu_dialog": 1,
            "notifications_permission_prompt": 2,
            "open_account": 2,
            "open_home_timeline": 1,
            "open_link": 1,
            "phone_verification": 4,
            "privacy_options": 1,
            "security_key": 3,
            "select_avatar": 4,
            "select_banner": 2,
            "settings_list": 7,
            "show_code": 1,
            "sign_up": 2,
            "sign_up_review": 4,
            "tweet_selection_urt": 1,
            "update_users": 1,
            "upload_media": 1,
            "user_recommendations_list": 4,
            "user_recommendations_urt": 1,
            "wait_spinner": 3,
            "web_modal": 1,
        },
    }
    response = session.post(
        onboarding_signup_url,
        headers=onboarding_headers,
        json=onboarding_signup_json,
        proxies=proxy_X,
        verify=False,
    )
    print(response.text)
    flow_token = response.json()["flow_token"]

    # Sync optouts (?)
    optout_url = "https://twitter.com:443/i/api/1.1/account/personalization/sync_optout_settings.json"
    session.post(
        optout_url, headers=optout_headers, proxies=proxy_X, verify=False
    )  # Ignore response

    # download javascript again (it's different), `_twitter_sess` cookie will not be changed
    js_chal = session.get(
        twitter_sess_url, headers=twitter_sess_header, proxies=proxy_X, verify=False
    )

    # client event 4, 5 - Signup
    triggered_4 = time_ms()
    triggered_5 = triggered_4 + random.randrange(100, 500)
    client_events = (
        [  # triggered_on, page, [element], [items], action, sequence_start_timestamp
            {
                "type": "client_event",
                "triggered_on": triggered_4,
                "event_namespace": {"page": "onboarding", "action": "show"},
                "sequence_start_timestamp": sequence_start,
            },
            {
                "type": "client_event",
                "triggered_on": triggered_5,
                "event_namespace": {
                    "page": "onboarding",
                    "element": "view",
                    "action": "impression",
                },
                "items": [{"token": flow_token, "name": "Signup"}],
                "sequence_start_timestamp": sequence_start,
            },
        ]
    )
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # client event 6 - onboarding
    triggered_6 = time_ms()
    client_events = [
        {
            "type": "client_event",
            "triggered_on": triggered_6,
            "event_namespace": {
                "page": "onboarding",
                "component": "signup",
                "element": "email",
                "action": "choose",
            },
            "sequence_start_timestamp": sequence_start,
        }
    ]
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # Check if email is available
    session.get(
        check_email_url.format(email_address),
        headers=check_email_header,
        proxies=proxy_X,
        verify=False,
    )  # TODO actually check email status from response

    # client event 7 - email_next_link
    triggered_7 = time_ms()
    client_events = (
        [  # triggered_on, page, [element], [items], action, sequence_start_timestamp
            {
                "type": "client_event",
                "triggered_on": triggered_7,
                "event_namespace": {
                    "page": "onboarding",
                    "element": "link",
                    "action": "click",
                },
                "items": [
                    {
                        "token": flow_token,
                        "name": "Signup",
                        "description": "email_next_link",
                    }
                ],
                "sequence_start_timestamp": sequence_start,
            }
        ]
    )
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # client event 8 - SignupSettingsListEmail
    triggered_8 = time_ms()
    client_events = (
        [  # triggered_on, page, [element], [items], action, sequence_start_timestamp
            {
                "type": "client_event",
                "triggered_on": triggered_8,
                "event_namespace": {
                    "page": "onboarding",
                    "element": "view",
                    "action": "impression",
                },
                "items": [{"token": flow_token, "name": "SignupSettingsListEmail"}],
                "sequence_start_timestamp": sequence_start,
            }
        ]
    )
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # client event 9 - SignupSettingsListEmail, next_link
    triggered_9 = time_ms()
    client_events = (
        [  # triggered_on, page, [element], [items], action, sequence_start_timestamp
            {
                "type": "client_event",
                "triggered_on": triggered_9,
                "event_namespace": {
                    "page": "onboarding",
                    "element": "link",
                    "action": "click",
                },
                "items": [
                    {
                        "token": flow_token,
                        "name": "SignupSettingsListEmail",
                        "description": "next_link",
                    }
                ],
                "sequence_start_timestamp": sequence_start,
            }
        ]
    )
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # Ask for verification code
    begin_verification_url = (
        "https://twitter.com:443/i/api/1.1/onboarding/begin_verification.json"
    )
    begin_verification_json = {
        "email": email_address,
        "display_name": username,
        "flow_token": flow_token,
    }
    session.post(
        begin_verification_url,
        headers=onboarding_headers,
        json=begin_verification_json,
        proxies=proxy_X,
        verify=False,
    )  # Ignore response

    # client events 10, 11, 12, 13, 14
    triggered_10 = time_ms()
    triggered_11 = triggered_10 + random.randrange(1500, 2000)
    triggered_12 = triggered_11 + random.randrange(1, 10)
    triggered_13 = triggered_12 + random.randrange(1, 10)
    triggered_14 = triggered_13 + random.randrange(1, 10)
    client_events = [
        {  # 10
            "type": "client_event",
            "triggered_on": triggered_10,
            "event_namespace": {  # TODO sometimes this event is invoked before asking for verification code
                "page": "onboarding",
                "element": "view",
                "action": "impression",
            },
            "items": [{"token": flow_token, "name": "SignupReview"}],
            "sequence_start_timestamp": sequence_start,
        },
        {  # 11
            "type": "client_event",
            "triggered_on": triggered_11,
            "event_namespace": {
                "page": "onboarding",
                "element": "link",
                "action": "click",
            },
            "items": [
                {
                    "token": flow_token,
                    "name": "SignupReview",
                    "description": "signup_with_email_next_link",
                }
            ],
            "sequence_start_timestamp": sequence_start,
        },
        {  # 12
            "type": "client_event",
            "triggered_on": triggered_12,
            "event_namespace": {
                "page": "onboarding",
                "element": "view",
                "action": "impression",
            },
            "items": [{"token": flow_token, "name": "EmailVerificationSubtaskLink"}],
            "sequence_start_timestamp": sequence_start,
        },
        {  # 13
            "type": "client_event",
            "triggered_on": triggered_13,
            "event_namespace": {
                "page": "onboarding",
                "element": "link",
                "action": "click",
            },
            "items": [{"token": flow_token, "name": "EmailVerificationSubtaskLink"}],
            "sequence_start_timestamp": sequence_start,
        },
        {  # 14
            "type": "client_event",
            "triggered_on": triggered_14,
            "event_namespace": {
                "page": "onboarding",
                "element": "view",
                "action": "impression",
            },
            "items": [{"token": flow_token, "name": "EmailVerification"}],
            "sequence_start_timestamp": sequence_start,
        },
    ]
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # Solve javascript challenge
    js_chal_response = solve_js_challenge(js_chal.text, driver)

    # Prepare heartbeat thread
    t = Thread(target=keepalive, args=(session,))
    t.start()

    # Get email verification code
    twitter_verif_code = input("Twitter verification code: ")
    G.kill = True  # Stop heartbeat

    # client event 15 - EmailVerification, next_link
    triggered_15 = time_ms()
    client_events = (
        [  # triggered_on, page, [element], [items], action, sequence_start_timestamp
            {
                "type": "client_event",
                "triggered_on": triggered_15,
                "event_namespace": {
                    "page": "onboarding",
                    "element": "link",
                    "action": "click",
                },
                "items": [
                    {
                        "token": flow_token,
                        "name": "EmailVerification",
                        "description": "next_link",
                    }
                ],
                "sequence_start_timestamp": sequence_start,
            }
        ]
    )
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # Send verification code + challenge response
    onboarding_send_code_string = '{{"flow_token": "{}", "subtask_inputs": [{{"subtask_id": "Signup", "sign_up": {{"js_instrumentation": {{"response": "{}"}}, "link": "email_next_link", "name": "{}", "email": "{}", "birthday": {{"day": {}, "month": {}, "year": {}}}}}}}, {{"subtask_id": "SignupSettingsListEmail", "settings_list": {{"setting_responses": [{{"key": "allow_emails_about_activity", "response_data": {{"boolean_data": {{"result": false}}}}}}, {{"key": "find_by_email", "response_data": {{"boolean_data": {{"result": false}}}}}}, {{"key": "personalize_ads", "response_data": {{"boolean_data": {{"result": false}}}}}}], "link": "next_link"}}}}, {{"subtask_id": "SignupReview", "sign_up_review": {{"link": "signup_with_email_next_link"}}}}, {{"subtask_id": "EmailVerification", "email_verification": {{"code": "{}", "email": "{}", "link": "next_link"}}}}]}}'.format(
        flow_token,
        js_chal_response,
        username,
        email_address,
        15,
        8,
        1996,
        twitter_verif_code,
        email_address,
    )
    response = session.post(
        onboarding_url,
        headers=onboarding_headers,
        data=onboarding_send_code_string,
        proxies=proxy_X,
        verify=False,
    )
    # Example of succesful email verification: TODO remove
    # {"flow_token":"g;160389851335133523:-1603898515311:Ndo239cQQ7kcizkfOfIdvV1r:2","status":"success","subtasks":[{"subtask_id":"EnterPassword","enter_password":{"primary_text":{"text":"You'll need a password","entities":[]},"next_link":{"link_type":"task","link_id":"next_link","label":"Next"},"secondary_text":{"text":"Make sure it’s 8 characters or more.","entities":[]},"hint":"Password","name":"armando07768","username":"armando07768","email":"armando07768@stempmail.com"},"progress_indication":{"text":{"text":"Step 5 of 5","entities":[]}}}]}

    if not response:
        print("[!] Error finalizing registration")
        print(response.text)
        return False
    finalize_json = response.json()
    if (
        not "subtasks" in finalize_json
        or len(finalize_json["subtasks"]) < 1
        or not "subtask_id" in finalize_json["subtasks"][0]
    ):
        print("[!] Missing Subtaks in response json during finalize, got:")
        print(response.text)
        return False
    if finalize_json["subtasks"][0]["subtask_id"] == "EnterPhoneForVerification":
        print("[!] SMS confirmation required. Try changing IP address")
        return False

    # client event 16 - EnterPassword
    triggered_16 = time_ms()
    client_events = (
        [  # triggered_on, page, [element], [items], action, sequence_start_timestamp
            {
                "type": "client_event",
                "triggered_on": triggered_16,
                "event_namespace": {
                    "page": "onboarding",
                    "element": "view",
                    "action": "impression",
                },
                "items": [{"token": flow_token, "name": "EnterPassword"}],
                "sequence_start_timestamp": sequence_start,
            }
        ]
    )
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # Check password strength
    password_strength_data = {
        "password": password,
        "username": username,
    }  # TODO check this is actually sent as URL parameters data
    session.post(
        password_strength_url,
        headers=optout_headers,
        data=password_strength_data,
        proxies=proxy_X,
        verify=False,
    )  # TODO do something with this response

    # client event 17 - entered_password
    triggered_17 = time_ms()
    client_events = (
        [  # triggered_on, page, [element], [items], action, sequence_start_timestamp
            {
                "type": "client_event",
                "triggered_on": triggered_17,
                "event_namespace": {
                    "page": "onboarding",
                    "component": "password_entry",
                    "element": "entered_password",
                    "action": "valid",
                },
                "sequence_start_timestamp": sequence_start,
            }
        ]
    )
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    # client event 18 - entered_password, click
    triggered_18 = time_ms()
    client_events = (
        [  # triggered_on, page, [element], [items], action, sequence_start_timestamp
            {
                "type": "client_event",
                "triggered_on": triggered_18,
                "event_namespace": {
                    "page": "onboarding",
                    "element": "link",
                    "action": "click",
                },
                "items": [
                    {
                        "token": flow_token,
                        "name": "EnterPassword",
                        "description": "next_link",
                    }
                ],
                "sequence_start_timestamp": sequence_start,
            }
        ]
    )
    success, client_event_sequence = send_twitter_client_event(
        session, client_events, client_event_sequence
    )

    enter_password_json = {
        "flow_token": flow_token,
        "subtask_inputs": [
            {
                "subtask_id": "EnterPassword",
                "enter_password": {"password": password, "link": "next_link"},
            }
        ],
    }
    response = session.post(
        onboarding_url,
        headers=onboarding_headers,
        data=enter_password_json,
        proxies=proxy_X,
        verify=False,
    )  # WARNING This request always yields an error (see response)

    print("SET PASSWORD REQUEST:")  # TODO remove
    print(enter_password_json)  # TODO remove
    print("SET PASSWORD RESPONSE:")  # TODO remove
    print(response.text)  # TODO remove

    print("[#] Successfully registered as {}:{}".format(email_address, password))

    return True


driver = webdriver.Chrome()

# print("\t[*] Session URL: {}".format(driver.command_executor._url))
# print("\t[*] Session ID: {}".format(driver.session_id))


class globalVars:
    pass


G = globalVars()  # empty object to pass around global state
G.kill = False

while True:
    session = requests.session()
    # Debug code
    # proxies = {
    # 	'http': 'http://127.0.0.1:8080',
    # 	'https': 'http://127.0.0.1:8080'
    # }
    # session.proxies.update(proxies)
    # session.verify = False

    registered = register_twitter(session)
    if registered:
        break

driver.get("http://twitter.com")
for cookie in session.cookies:
    print(cookie)
for cookie in session.cookies:
    driver.add_cookie(
        {
            "name": cookie.name,
            "value": cookie.value,
            "path": cookie.path,
            "domain": cookie.domain,
        }
    )
