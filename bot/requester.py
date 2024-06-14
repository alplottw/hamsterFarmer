import requests


class Requester:
    def __init__(self, account):
        self.proxy_url = f"http://{account['proxy']}"
        self.base_url = 'https://api.hamsterkombat.io'
        self.headers = {
            'Authorization': f"Bearer {account['token']}",
            'User-Agent': account['useragent'],
            # 'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Windows"'
        }
        self._proxy_test()
        self.session = requests.Session()
        self.session.proxies = {
            'http': self.proxy_url,
        }

    def _proxy_test(self):
        proxies = {
            'http': self.proxy_url,
        }
        url = 'http://httpbin.org/ip'

        try:
            response = requests.get(url, proxies=proxies)
            print("IP Address:", response.json()['origin'])
        except requests.exceptions.ProxyError as e:
            print("Proxy error:", e)
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

    def _send_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint
        try:
            if method == 'GET':
                response = self.session.get(url, headers=self.headers)
            elif method == 'POST':
                response = self.session.post(url, headers=self.headers, data=data)
            elif method == 'PUT':
                response = self.session.put(url, headers=self.headers)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=self.headers)
            else:
                return f"Unsupported HTTP method: {method}"

            if response.status_code == 200:
                return response.json()
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Request error: {e}"

    def auth_me_telegram(self):
        return self._send_request('POST', '/auth/me-telegram')

    def clicker_config(self):
        return self._send_request('POST', '/clicker/config')

    def clicker_sync(self):
        return self._send_request('POST', '/clicker/sync')

    def clicker_upgrades_for_buy(self):
        return self._send_request('POST', '/clicker/upgrades-for-buy')

    def clicker_list_tasks(self):
        return self._send_request('POST', '/clicker/list-tasks')

    def clicker_list_airdrop_tasks(self):
        return self._send_request('POST', '/clicker/list-airdrop-tasks')

    def clicker_tap(self, data):
        self.headers['Content-Type'] = 'application/json'
        response = self._send_request('POST', '/clicker/tap', data)
        del self.headers['Content-Type']
        return response

    def clicker_boosts_for_buy(self):
        return self._send_request('POST', '/clicker/boosts-for-buy')

    def clicker_buy_boost(self, data):
        self.headers['Content-Type'] = 'application/json'
        response = self._send_request('POST', '/clicker/buy-boost', data)
        del self.headers['Content-Type']
        return response

    def clicker_buy_upgrade(self, data):
        self.headers['Content-Type'] = 'application/json'
        response = self._send_request('POST', '/clicker/buy-upgrade', data)
        del self.headers['Content-Type']
        return response
