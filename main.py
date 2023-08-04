# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Req import Account, TwitMethods, UploadFile
from twitter import TwitterPost


def print_hi(name):
    proxy = "krishnae:Ideapads340@5.42.76.76:1080"
    cooks = {
        "ct0": "fda5e4f3f281142c6725145c8edb49ed9a1086cc9bc0d9462a08aa75b0a4cfdf5d132e1884f108f16f9e866d17adf20d5afb3d1bc2545553dfea20e83765d197d77057085823a6ade119b280eaeaa4ab",
        "auth_token": "18d522e98d1ad83617575e874291b2b09d9ded05",
    }
    # print(UploadFile.upload_file(cooks, "video.mp4", proxy))
    # print(TwitMethods.get_request_data(10, "test"))
    print(TwitterPost.post(cooks, text="Test string", media="video.mp4", proxy=proxy))


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("PyCharm")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
