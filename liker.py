from twit_func import TwitMethods
class Accounts:
    def __init__(self):
        self.accs = self.file_read()


    def file_read(self):
        with open("accs.txt", 'r') as file:
            content = file.readlines()
            return content



class Proxy:
    def __init__(self):
        self.proxy = "krishnae:Ideapads340@5.42.76.76:1080"

class Account:
    def __init__(self, data: str):
        self.cooks = self.parse_cooks(data)

    def parse_cooks(self, data: str):
        data = data.split(":")
        return {"ct0": data[1], "auth_token": data[0]}



class Worker:
    def __init__(self, accs: Accounts):
        accs = accs

    def work(self, accs: Accounts):
        for acc in accs.accs:
            account = Account(acc)
            if TwitMethods.valid_check(account.cooks, Proxy().proxy) == 1:
                


if __name__ == '__main__':
    Worker(Accounts())
