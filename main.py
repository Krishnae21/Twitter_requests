# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Req import Account


def print_hi(name):
    Acc = Account(
        {
            "ct0": "145266abb52a8635d2ba9582aa1aade4cd1aa8d392f67219b021240223834e90409db844cf3688b06afd52377cc45046014690588e39f058a81d1d7cb3c069998962549671887032c155d458a955af8a",
            "auth_token": "d9c9d9a5ffd31c8d1aca444ea6bdaed90d1a4cc4",
        }
    )
    # Acc.retweet(tweetId='1682781278481858560')
    print(Acc.get_latest_tweets("porn", 30))


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("PyCharm")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
