# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Req import Account, TwitMethods, UploadFile


def print_hi(name):
    # Acc = Account(
    #     {
    #         "ct0": "145266abb52a8635d2ba9582aa1aade4cd1aa8d392f67219b021240223834e90409db844cf3688b06afd52377cc45046014690588e39f058a81d1d7cb3c069998962549671887032c155d458a955af8a",
    #         "auth_token": "d9c9d9a5ffd31c8d1aca444ea6bdaed90d1a4cc4",
    #     }
    # )
    # # Acc.retweet(tweetId='1682781278481858560')
    # print(Acc.get_latest_tweets("porn", 30))
    proxy = 'krishnae:Ideapads340@5.42.76.76:1080'
    cooks = {"ct0": '3f3febc252a6f272efb19db5a5de8e249d71d89b10a37d73ea7509869917dd5f09a896d4e3694c2198247b406f515e736ae862b1df7b65241336c55216284136f0c110c19d7cc66f604e8da57235b122', "auth_token": '18d522e98d1ad83617575e874291b2b09d9ded05'}
    # rez = TwitMethods.cookies_check(cooks, proxy)
    # print(rez)
    # print(TwitMethods.movieSize('video.mp4'))
    print(UploadFile.upload_file(cooks, 'video.mp4', proxy))
# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("PyCharm")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
