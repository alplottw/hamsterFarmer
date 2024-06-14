import bot


class Hamster():
    def __init__(self, account):
        self.requester = bot.Requester(account)
        self.auth_me_telegram = self.requester.auth_me_telegram()
        self.clicker_config = self.requester.clicker_config()
        self.clicker_sync = self.requester.clicker_sync()
        self.clicker_upgrades_for_buy = self.requester.clicker_upgrades_for_buy()
        self.clicker_list_tasks = self.requester.clicker_list_tasks()
        self.clicker_list_airdrop_tasks = self.requester.clicker_list_airdrop_tasks()

        self.clicker = bot.Clicker(self.clicker_sync['clickerUser'], self.requester, account['id'])
        self.upgrader = bot.Upgrader(self.clicker_sync['clickerUser'], self.clicker_upgrades_for_buy,
                                     self.requester, account['id'])

    def run(self):
        self.clicker.run()
        self.upgrader.run()
