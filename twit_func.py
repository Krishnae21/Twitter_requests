import requests
import sys
from moviepy.editor import VideoFileClip
import os
import json
import time




class TwitMethods:
    @staticmethod
    def parser_twit_result(data: str):
        try:
            data = json.loads(data)
            return {
                "id": data.get("data")
                .get("create_tweet")
                .get("tweet_results")
                .get("result")
                .get("rest_id"),

                "username": data.get("data")
                .get("create_tweet")
                .get("tweet_results")
                .get("result")
                .get("core")
                .get("user_results")
                .get("result")
                .get("legacy")
                .get("screen_name"),
            }

        except Exception:
            return None

    @staticmethod
    def cookies_check(cookies: dict, proxy: str = None) -> dict:
        if cookies.get("ct0") and cookies.get("auth_token"):
            valid = TwitMethods.valid_check(cookies, proxy)
            if valid == 1:
                return {"status": True, "message": "", "code": 0}
            elif valid == 2:
                return {"status": False, "message": "Account is blocked", "code": 2}
            elif valid == 3:
                return {"status": False, "message": "", "code": 3}
        else:
            return {"status": False, "message": "Not found Cookies", "code": 1}

    @staticmethod
    def valid_check(cookies: dict, proxy: str = None):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
            "Accept": "*/*",
            "Referer": "https://twitter.com",
            "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "X-Csrf-Token": cookies.get("ct0"),
            "X-Twitter-Active-User": "yes",
            "X-Twitter-Client-Language": "en",
        }
        if proxy:
            proxy = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
        url: str = "https://twitter.com/i/api/1.1/branch/init.json"
        response = requests.post(
            url, cookies=cookies, headers=headers, json={}, proxies=proxy, verify=False
        )
        if response.status_code == 403:
            # Блок
            return 2
        elif response.status_code == 200:
            # Валид
            return 1
        else:
            print(response)
            return 3

    @staticmethod
    def movie_duration(filepath: str):
        clip = VideoFileClip(filepath)
        duration = clip.duration * 1000 + 10
        clip.close()
        return duration

    @staticmethod
    def movie_size(filepath: str):
        return os.stat(filepath).st_size

    @staticmethod
    def proxy(proxy: str):
        if proxy:
            proxy = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        else:
            proxy = None
        return proxy

    @staticmethod
    def get_headers(cookies: dict):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
            "Accept": "*/*",
            "Referer": "https://twitter.com",
            "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "X-Csrf-Token": cookies.get("ct0"),
            "X-Twitter-Active-User": "yes",
            "X-Twitter-Client-Language": "en",
        }

    @staticmethod
    def get_request_data(media_id: int = None, text: str = None):
        data = json.loads(
            """{"variables":{"tweet_text":"","dark_request":false,"media":{"media_entities":[],"possibly_sensitive":false},"semantic_annotation_ids":[]},"features":{"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_enhance_cards_enabled":false},"queryId":"SoVnbfCycZ7fERGCwpZkYA"}"""
        )
        if media_id:
            data["variables"]["media"]["media_entities"].append(
                {"media_id": str(media_id), "tagged_users": []}
            )
        if text:
            data["variables"]["tweet_text"] = text
        return data
        # return res


class UploadFile:
    url = "https://upload.twitter.com/i/media/upload.json"

    @staticmethod
    def upload_file(cookies: dict, filepath: str, proxy: dict):
        duration = TwitMethods.movie_duration(filepath)
        size = TwitMethods.movie_size(filepath)
        init_status = UploadFile.load_init(cookies, proxy, size, duration)

        if init_status.get("status"):
            if UploadFile.send_file(filepath, proxy, cookies, init_status.get("id")).get("status"):
                if UploadFile.load_finalize(proxy, cookies, init_status.get("id")).get("status"):
                    return {"status": True, "id": init_status.get("id")}
        return {"status": False}

    @staticmethod
    def load_init(cookies: dict, proxy: dict, size: int, duration: float):
        data = {
            "command": "INIT",
            "total_bytes": size,
            "media_type": "video/mp4",
            "video_duration_ms": duration,
            "media_category": "tweet_video",
        }
        try:
            res = requests.post(
                UploadFile.url,
                data=data,
                params=data,
                proxies=proxy,
                cookies=cookies,
                headers=TwitMethods.get_headers(cookies),
                timeout=5,
                verify=False
            )
            if res.status_code == 202:
                response = json.loads(res.text)
                return {"status": True, "id": response.get("media_id")}
            else:
                return {
                    "status": False,
                    "message": "Status code error",
                    "data": [res.status_code, res.text],
                }
        except Exception as ex:
            return {"status": False, "message": "Exception", "data": ex}

    @staticmethod
    def send_file(filepath: str, proxy: dict, cookies: dict, media_id: int):
        status = True
        segment_index: int = 0
        data = {"command": "APPEND", "media_id": media_id, "segment_index": 0}
        try:
            with open(filepath, "rb") as file:
                segment_size = 1024 * 1024 * 1
                while status:
                    segment = file.read(segment_size)
                    if not segment:
                        break
                    data["segment_index"] = segment_index
                    files = {"media": segment}
                    response = requests.post(
                        UploadFile.url,
                        headers=TwitMethods.get_headers(cookies),
                        params=data,
                        proxies=proxy,
                        data=data,
                        files=files,
                        cookies=cookies,
                        verify=False
                    )

                    if response.status_code == 204:
                        segment_index += 1
                    else:
                        status = False
            return {"status": status}
        except Exception as ex:

            return {"status": False, "message": "Exception", "data": ex}

    @staticmethod
    def load_finalize(proxy: dict, cookies: dict, media_id: int):
        data = {"command": "FINALIZE", "media_id": media_id, "allow_async": True}
        try:
            res = requests.post(
                UploadFile.url,
                proxies=proxy,
                data=data,
                params=data,
                cookies=cookies,
                headers=TwitMethods.get_headers(cookies),
                verify=False
            )
            if res.status_code == 200:
                return {"status": True}
            else:
                return {
                    "status": False,
                    "message": "Status code error",
                    "data": [res.status_code, res.text],
                }
        except Exception as ex:
            return {"status": False, "message": "Exception", "data": ex}

    @staticmethod
    def load_status(proxy: dict, cookies: dict, media_id: int):
        wait = 0
        data = {"command": "STATUS", "media_id": media_id}
        try:
            while True:
                time.sleep(wait)
                res = requests.get(
                    UploadFile.url,
                    headers=TwitMethods.get_headers(cookies),
                    cookies=cookies,
                    params=data,
                    proxies=proxy,
                    verify=False
                )
                if res.status_code == 200:
                    response = json.loads(res.text)
                    if response.get("processing_info").get("state") == "in_progress":
                        wait = response.get("processing_info").get("check_after_secs")
                    elif response.get("processing_info").get("state") == "succeeded":
                        return {"status": True}
                    else:
                        return {
                            "status": False,
                            "message": "Error response",
                            "data": response,
                        }
                else:
                    return {
                        "status": False,
                        "message": "Status code error",
                        "data": res.text,
                    }
        except Exception as ex:
            return {"status": False, "message": "Exception", "data": ex}
