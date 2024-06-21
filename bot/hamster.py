import bot
from bot import config
from bot.utils import save_json_to_file, log, create_directory_structure


class Hamster():
    def __init__(self, account):
        self.account = account
        self.requester = bot.Requester(self.account)
        self.auth_me_telegram = self.requester.auth_me_telegram()
        self.clicker_config = self.requester.clicker_config()
        self.clicker_sync = self.requester.clicker_sync()
        self.clicker_upgrades_for_buy = self.requester.clicker_upgrades_for_buy()
        self.clicker_list_tasks = self.requester.clicker_list_tasks()
        self.clicker_list_airdrop_tasks = self.requester.clicker_list_airdrop_tasks()

        create_directory_structure()
        save_json_to_file(self.auth_me_telegram, './logs/auth_me_telegram.json')
        save_json_to_file(self.clicker_config, './logs/clicker_config.json')
        save_json_to_file(self.clicker_sync, './logs/clicker_sync.json')
        save_json_to_file(self.clicker_upgrades_for_buy, './logs/clicker_upgrades_for_buy.json')
        save_json_to_file(self.clicker_list_tasks, './logs/clicker_list_tasks.json')
        save_json_to_file(self.clicker_list_airdrop_tasks, './logs/clicker_list_airdrop_tasks.json')

    def run(self):

        # log(self.account['id'], self.getBalance(self.clicker_sync))

        if config.COLLECT_DAILY:
            self.claim_daily_reward()

        self.clicker = bot.Clicker(self.clicker_sync['clickerUser'], self.requester, self.account['id'])

        if config.COLLECT_CIPHER:
            if not self.clicker.cipher_is_claim(self.clicker_config):
                log(self.account['id'], {"cipher": "not claimed"})
                if self.clicker.cipher_claim():
                    log(self.account['id'], {"cipher": "claimed"})
            else:
                log(self.account['id'], {"cipher": "claimed"})

        if config.COLLECT_CLICKS:
            self.clicker_sync['clickerUser'] = self.clicker.run()

        self.upgrader = bot.Upgrader(self.clicker_sync['clickerUser'], self.clicker_upgrades_for_buy,
                                     self.requester, self.account['id'])

        if config.COLLECT_COMBO:
            if self.upgrader.is_claim_combo() and len(config.DAILY_CARD_COMBO) > 0:
                log(self.account['id'], {"combo": "not claimed"})
                self.upgrader.claim_combo(config.DAILY_CARD_COMBO)

        if config.COLLECT_UPGRADES:
            self.clicker_sync['clickerUser'] = self.upgrader.run()

        log(self.account['id'], self.getBalance(self.clicker_sync))

    def getBalance(self, clicker_sync):
        return {
            "balanceCoins": int(clicker_sync['clickerUser']['balanceCoins']),
            "earnPassivePerHour": int(clicker_sync['clickerUser']['earnPassivePerHour']),
            "lastPassiveEarn": int(clicker_sync['clickerUser']['lastPassiveEarn'])
        }

    def claim_daily_reward(self):
        self.clicker_list_tasks = self.requester.clicker_list_tasks()

        for item in self.clicker_list_tasks['tasks']:
            if item['id'] == config.DAILY_REWARD_ID:
                break

        if not item['isCompleted']:
            log(self.account['id'], {"daily reward": "not claimed"})
            item = self.requester.claim_daily_reward()['task']

        if item['isCompleted']:
            self.requester.clicker_list_tasks()
            self.requester.clicker_upgrades_for_buy()
            log(self.account['id'], {"daily reward": "claimed"})
