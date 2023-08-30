class Account:
    # Status:
    #   0: Куки без токенов
    #   1: Куки невалид
    #   2: Куки валид
    #   3: Акк в блоке
    #   4: Каптча, надо допилить
    def __init__(self, cookies: dict):
        self.cookies: dict = {}
        self.status: int = 0
        self.add_cookies(cookies)

    def add_cookies(self, cookies: dict) -> dict:
        # Проверка куки на наличие токенов
        # Переформатирование куки внутри класса для большего удобства
        # Создание класса для запросов

        self.cookies["ct"] = cookies.get("ct0")
        self.cookies["token"] = cookies.get("auth_token")
        if self.cookies.get("ct") and self.cookies.get("token"):
            self.Req = TwitRequests(self.cookies)
            self.status = self.Req.check_acc()
        else:
            self.status = 0
            return 0

    def check_cookie(self):
        # Проверка куки на валидность
        # Запись результата в переменную статус
        res = self.Req.check_acc()
        self.status = res.get("Status")
        return self.status

    def retweet(self, tweetId: str):
        rez = self.Req.retweet(tweetId)
        return rez

    def get_latest_tweets(self, query: str, count: int):
        self.Req.get_latest_tweets(query, count)


class TwitRequests:
    def __init__(self, cookies: dict):
        self.cookies = cookies
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
            "Accept": "*/*",
            "Referer": "https://twitter.com",
            "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "X-Csrf-Token": self.cookies.get("ct"),
            "X-Twitter-Active-User": "yes",
            "X-Twitter-Client-Language": "en",
        }
        self.COOKIES = {
            "auth_token": self.cookies.get("token"),
            "ct0": self.cookies.get("ct"),
        }

    def check_acc(self):
        URL1 = "https://api.twitter.com/1.1/account/settings.json?include_mention_filter=true&include_nsfw_user_flag=true&include_nsfw_admin_flag=true&include_ranked_timeline=true&include_alt_text_compose=true&ext=ssoConnections&include_country_code=true&include_ext_dm_nsfw_media_filter=true&include_ext_sharing_audiospaces_listening_data_with_followers=true"
        URL2 = "https://twitter.com/i/api/1.1/branch/init.json"
        response = requests.get(URL1, cookies=self.COOKIES, headers=self.HEADERS)
        # resp_json = response.json()
        if response.status_code == 401:
            # Невалид
            return 1
        elif response.status_code == 200:
            response = requests.post(
                URL2, cookies=self.COOKIES, headers=self.HEADERS, json={}
            )
            if response.status_code == 403:
                # Блок
                return 3
            elif response.status_code == 200:
                # Валид
                return 2

        # Печать ошибки в поток stderr
        print(response.json(), file=sys.stderr)

    def retweet(self, tweetId: str):
        URL_RETWEET = (
            "https://twitter.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet"
        )
        queryId = "ojPdsZsimiJrUGLR1sjUtA"
        data = {
            "variables": {"tweet_id": tweetId, "dark_request": False},
            "queryId": queryId,
        }

        response = requests.post(
            URL_RETWEET, cookies=self.COOKIES, headers=self.HEADERS, json=data
        )
        status_code = response.status_code
        response = response.json()
        if status_code == 200:
            code = response.get("errors")
            if code is None:
                if (
                    response.get("data")
                    .get("create_retweet")
                    .get("retweet_results")
                    .get("result")
                    .get("rest_id")
                ):
                    # Успешно
                    return 2
            else:
                code = code[0].get("code")
                if code == 327 or code == 144:
                    # Ошибка: Already retweeted or bad id
                    return 1
                elif code == 37:
                    # Ошибка: Акк забанили(
                    return 3

        # Печать ошибки в поток stderr
        print(response, file=sys.stderr)
        # print(response.status_code)
        print(response)

    def get_latest_tweets(self, query: str, count: int):
        URL = (
            '''https://twitter.com/i/api/graphql/NA567V_8AFwu0cZEkAAKcw/SearchTimeline?variables={"rawQuery":"'''
            + query
            + """'","count":20,"querySource":"recent_search_click","product":"Latest"}&features={"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withAuxiliaryUserLabels":false,"withArticleRichContentState":false}"""
        )

        cursor: str = ""
        CURSOR_URL = (
            'https://twitter.com/i/api/graphql/NA567V_8AFwu0cZEkAAKcw/SearchTimeline?variables={"rawQuery":"'
            + query
            + '","count":20,"cursor":"'
            + cursor
            + '","querySource":"recent_search_click","product":"Latest"}&features={"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withAuxiliaryUserLabels":false,"withArticleRichContentState":false}'
        )

        tweets: list = []
        response = requests.get(URL, headers=self.HEADERS, cookies=self.COOKIES)
        if response.status_code == 200:
            try:
                response_tweets = (
                    response.json()
                    .get("data")
                    .get("search_by_raw_query")
                    .get("search_timeline")
                    .get("timeline")
                    .get("instructions")
                )
                items = response_tweets[0].get("entries")

                for item in items:
                    if item.get("entryId").find("tweet") != -1:
                        tweet_id: str = item.get("entryId")[6:]
                        tweets.append(tweet_id)
                    elif item.get("entryId").find("cursor-bottom-0") != -1:
                        cursor = item.get("content").get("value")

                while len(tweets) < count and len(cursor) > 1:
                    response = requests.get(
                        self.new_url(query, cursor),
                        headers=self.HEADERS,
                        cookies=self.COOKIES,
                    )
                    if response.status_code == 200:
                        instr = (
                            response.json()
                            .get("data")
                            .get("search_by_raw_query")
                            .get("search_timeline")
                            .get("timeline")
                        )
                        items = instr.get("instructions")[0].get("entries")
                        rez_parser = self.tweets_parser(tweets, items)
                        if rez_parser == 1:
                            cursor = (
                                instr.get("instructions")[2]
                                .get("entry")
                                .get("content")
                                .get("value")
                            )

                print(len(tweets))
                print(tweets)
                return tweets
            except Exception:
                return tweets
        return None

    def tweets_parser(self, tweets: list, response_tweets: list) -> int:
        try:
            for item in response_tweets:
                if item.get("entryId").find("tweet") != -1:
                    tweets.append(item.get("entryId")[6:])

            print(tweets)
            return 1
        except Exception:
            return 0

    def new_url(self, query, cursor):
        return (
            'https://twitter.com/i/api/graphql/NA567V_8AFwu0cZEkAAKcw/SearchTimeline?variables={"rawQuery":"'
            + query
            + '","count":20,"cursor":"'
            + cursor
            + '","querySource":"recent_search_click","product":"Latest"}&features={"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withAuxiliaryUserLabels":false,"withArticleRichContentState":false}'
        )
