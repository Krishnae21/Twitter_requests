task_url = "https://api.twitter.com/1.1/onboarding/task.json"

onboarding_headers = {
    "Connection": "close",
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "X-twitter-client-language": "en",
    # "x-csrf-token": "54b9d9e87a4fef1889d060be00437558",
    # "x-guest-token": "1321170979104632838",
    "X-twitter-active-user": "yes",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    # "content-type": "application/json",
    "Accept": "*/*",
    "Origin": "https://twitter.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://twitter.com/i/flow/signup",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}


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