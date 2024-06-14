import threading

import bot
from bot import config
from bot.utils import read_account_from_file, delay


def start(account):
    bot.Hamster(account).run()


if __name__ == '__main__':
    accounts = read_account_from_file()
    for account in accounts:
        thread = threading.Thread(target=start, args=(account,))
        thread.start()
        delay(config.MIN_DELAY, config.MAX_DELAY)
