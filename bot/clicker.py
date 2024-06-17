import json
import random

from bot import config
from bot.utils import get_timestamp, get_date_time, delay, log


class Clicker:
    def __init__(self, clicker_user, requestor, account_id):
        self.clicker_user = clicker_user
        self.requester = requestor
        self.count = 0
        self.account_id = account_id

    def run(self):
        while self.clicker_user['availableTaps'] > config.MAX_CLICK / self.clicker_user['earnPerTap']:
            self._tap()

        id = self._check_boost_cooldown()
        if id:
            self._buy_boost(id)
            self.run()

        return self.clicker_user

    def _get_tap_data(self):
        count = random.randint(config.MIN_CLICK, config.MAX_CLICK)
        data = {
            "availableTaps": self.clicker_user['availableTaps'],
            "count": int(count / self.clicker_user['earnPerTap']),
            "timestamp": get_timestamp(),
        }
        if data['availableTaps'] < data['count'] * self.clicker_user['earnPerTap']:
            data['count'] = int(data['availableTaps'] / self.clicker_user['earnPerTap']) - 10

        self.count += data['count'] * self.clicker_user['earnPerTap']

        text = f"{get_date_time()} | id: {self.account_id} | clicked: {self.count}"
        log(self.account_id, text)
        print(text)

        return data

    def _tap(self):
        delay(25, 40)

        tap_data = self._get_tap_data()
        response = self.requester.clicker_tap(json.dumps(tap_data))

        if 'clickerUser' in response:
            self.clicker_user = response['clickerUser']

    def _check_boost_cooldown(self):
        id_to_find = config.BOOST_ID
        item = find_by_id(self.requester.clicker_boosts_for_buy(), id_to_find)

        if item['cooldownSeconds'] == 0:
            return item['id']
        return False

    def _buy_boost(self, id):
        data = {
            "boostId": id,
            "timestamp": get_timestamp(),
        }
        response = self.requester.clicker_buy_boost(json.dumps(data))
        self.clicker_user = response['clickerUser']


def find_by_id(data, id):
    for item in data.get('boostsForBuy', []):
        if item.get('id') == id:
            return item
    return None
