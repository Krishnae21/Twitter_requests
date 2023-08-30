import requests
import json
from twit_func import TwitMethods, UploadFile
import time


class TwitterPost:
    @staticmethod
    def post(cookies: dict, text: str = None, media: str = None, proxy: str = None):
        url = "https://twitter.com/i/api/graphql/SoVnbfCycZ7fERGCwpZkYA/CreateTweet"
        media_id = None
        if proxy:
            proxy = TwitMethods.proxy(proxy)
        if media:
            media_status = UploadFile.upload_file(cookies, media, proxy)

            if media_status.get("status") == False:
                print(media_status)
                return {
                    "status": False,
                    "message": "Media load error",
                    "data": media_status,
                }
            else:
                print("Good | ", media_status)
                media_id = media_status.get("id")
        data = TwitMethods.get_request_data(media_id, text)
        print(data)
        headers = TwitMethods.get_headers(cookies)
        try:
            if UploadFile.load_status(proxy,cookies, media_id):

                res = requests.post(
                    url, proxies=proxy, headers=headers, cookies=cookies, json=data, verify=False
                )
                print(res.status_code)
                print(res.text)
                if res.status_code == 200:
                    results = TwitMethods.parser_twit_result(res.text)
                    post_id = results.get("id")
                    username = results.get("username")
                    return {"status": True,"data": {"post_id": post_id, "username": username}}
                else:
                    print(res.status_code)
                    print(res.text)
        except Exception as ex:
            return {"status": False, "data": ex}
