import json
import random

from bot import config
from bot.utils import get_timestamp, delay, log


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
        return self.clicker_user

    def _buy_upgrade(self, upgrade):
        data = {
            "timestamp": get_timestamp(),
            "upgradeId": upgrade['id']
        }

        log(self.account_id, {"name": upgrade['name'], "level": upgrade['level'], "price": upgrade['price']})

        response = self.requester.clicker_buy_upgrade(json.dumps(data))
        self.clicker_upgrades_for_buy['upgradesForBuy'] = response['upgradesForBuy']
        self.clicker_user = response['clickerUser']

        delay(5, 10)

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

        is_random = random.randint(0, 1)
        if is_random:
            return result[random.randint(1, 4)]
        return result[0]

    def is_claim_combo(self):
        is_claimed = self.clicker_upgrades_for_buy['dailyCombo']['isClaimed']

        if is_claimed:
            log(self.account_id, {"combo": "claimed"})
            return False

        if not is_claimed:
            summ_price_combo = 0
            combo = config.DAILY_CARD_COMBO
            upgrades = []

            for upgrade_id in combo:
                upgrades.append(self.get_upgrade_by_id(upgrade_id))

            is_available = True
            for upgrade in upgrades:
                summ_price_combo += upgrade['price']
                if not self._check_upgrade(upgrade):
                    is_available = False
                    break

            if summ_price_combo > self.clicker_user['balanceCoins']:
                is_available = False
            if summ_price_combo > config.DAILY_CARD_COMBO_MAX_PRICE:
                is_available = False

            return is_available

        return False

    def claim_combo(self, combo):
        upgrades = []

        for upgrade_id in combo:
            upgrades.append(self.get_upgrade_by_id(upgrade_id))

        for upgrade in upgrades:
            self._buy_upgrade(upgrade)

        self.requester.claim_daily_combo()
        log(self.account_id, {"combo": "claimed"})

    def get_upgrade_by_id(self, id):
        for item in self.clicker_upgrades_for_buy.get('upgradesForBuy', []):
            if item.get('id') == id:
                return item

    def _check_upgrade(self, upgrade):
        result = True
        if not upgrade['profitPerHourDelta']:
            result = False
        if not upgrade['isAvailable']:
            result = False
        if upgrade['isExpired']:
            result = False
        if "cooldownSeconds" in upgrade:
            if upgrade['cooldownSeconds']:
                result = False

        return result
