import json

from bot.utils import get_timestamp, get_date_time, delay, log


class Upgrader:

    def __init__(self, clicker_user, clicker_upgrades_for_buy, requestor, account_id):
        self.clicker_user = clicker_user
        self.clicker_upgrades_for_buy = clicker_upgrades_for_buy
        self.requester = requestor
        self.account_id = account_id

    def run(self):
        upgrade = self._get_upgrade(self.clicker_upgrades_for_buy['upgradesForBuy'])
        while upgrade['price'] < self.clicker_user['balanceCoins']:
            self._buy_upgrade(upgrade)
            upgrade = self._get_upgrade(self.clicker_upgrades_for_buy['upgradesForBuy'])
            delay(5, 10)

    def _buy_upgrade(self, upgrade):
        data = {
            "timestamp": get_timestamp(),
            "upgradeId": upgrade['id']
        }
        text = f"{get_date_time()} | id: {self.account_id} | name: {upgrade['name']} | level: {upgrade['level']} | price: {upgrade['price']} | earnPassivePerHour: {self.clicker_user['earnPassivePerHour']}"
        log(self.account_id, text)
        print(text)

        response = self.requester.clicker_buy_upgrade(json.dumps(data))

        self.clicker_upgrades_for_buy['upgradesForBuy'] = response['upgradesForBuy']
        self.clicker_user = response['clickerUser']

    def _get_upgrade(self, upgrades):
        buf = []
        for upgrade in upgrades:
            if not upgrade['profitPerHourDelta']:
                continue
            if not upgrade['isAvailable']:
                continue
            if upgrade['isExpired']:
                continue
            if "cooldownSeconds" in upgrade:
                if upgrade['cooldownSeconds']:
                    continue

            upgrade['profit'] = upgrade['price'] / upgrade['profitPerHourDelta']
            buf.append(upgrade)

        result = sorted(buf, key=lambda x: x['profit'])
        return result[0]
