import requests
from requests import Request


def get_tokens():
    proxy = {"https": "http://08aabb2b-499363:1vsmxacrhz@93.190.142.57:42361"}
    payload = """category=perftown&log=%5B%7B%22description%22%3A%22rweb%3Ascroller%3Attfv%3Ascroller_v3%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A84%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AconversationGraphQL%3Afetch_Initial%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A1320%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AconversationGraphQL%3Afetch_Initial%3Aformat%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A1323%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AhomeGraphQL%3Afetch_Top%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A1847%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AhomeGraphQL%3Afetch_Top%3Aformat%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A1855%7D%2C%7B%22description%22%3A%22rweb%3Aseen_ids%3Apersistence%3Aset%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A270%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AconversationGraphQL%3Afetch_Bottom%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A1088%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AconversationGraphQL%3Afetch_Bottom%3Aformat%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A1089%7D%2C%7B%22description%22%3A%22rweb%3Ascroller%3Attfv%3Ascroller_v3%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A125%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AfavoritersGraphQL%3Afetch_Initial%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A324%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AfavoritersGraphQL%3Afetch_Initial%3Aformat%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A325%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AfavoritersGraphQL%3Afetch_Bottom%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A418%7D%2C%7B%22description%22%3A%22rweb%3Aurt%3AfavoritersGraphQL%3Afetch_Bottom%3Aformat%3Asuccess%22%2C%22product%22%3A%22rweb%22%2C%22duration_ms%22%3A419%7D%5D"""

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://twitter.com",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    }

    with open("accs.txt", "r") as file:
        listT = file.readlines()
        i = 0
        while i < len(listT):
            try:
                line = listT[i]
                COOKIES = {"auth_token": line.replace("\n", "")}
                response = requests.post(
                    "https://api.twitter.com/1.1/jot/client_event.json?keepalive=false",
                    cookies=COOKIES,
                    json=payload,
                    proxies=proxy,
                    headers=HEADERS,
                )
                # print(response.cookies)
                cookie = response.cookies.get("ct0")
                print(COOKIES.get("auth_token") + ":" + response.cookies.get("ct0"))
                i+=1
            except Exception as ex:
                x = 0


    #
    # for line in file:
    #         tokens: list.append(line)
    #         COOKIES = {"auth_token": line.replace("\n", "")}
    #         response = requests.post(
    #             "https://api.twitter.com/1.1/jot/client_event.json?keepalive=false",
    #             cookies=COOKIES,
    #             json=payload,
    #             proxies=proxy,
    #             headers=HEADERS,
    #         )
    #         # print(response.cookies)
    #         cookie = response.cookies.get("ct0")
    #         print(COOKIES.get("auth_token") + ":" + response.cookies.get("ct0"))


if __name__ == "__main__":
    get_tokens()
