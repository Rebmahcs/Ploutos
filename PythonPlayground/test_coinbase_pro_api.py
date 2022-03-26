from dotenv import dotenv_values
import hmac, hashlib, time, requests, base64
from requests.auth import AuthBase


def welcome():
    print("Starting Ploutos project. - Coinbase PRO version \n")


#Coinbase Clients
class CoinbasePRO:
    def __init__(self, sandbox=True):
        coinbase_conf = dotenv_values(".env.coinbase-pro.test" if sandbox else ".env.coinbase-pro")
        self.__auth = CoinbaseExchangeAuth(coinbase_conf["API_KEY"],
                                           coinbase_conf["API_SECRET"],
                                           coinbase_conf["API_PASSPHRASE"])
        self.__api = "https://api-public.sandbox.pro.coinbase.com/" if sandbox else "https://api.pro.coinbase.com/"

    def get(self, endpoint):
        return requests.get(self.__api + endpoint, auth=self.__auth)


# Custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, key, secret, passphrase):
        self.api_key = key
        self.secret_key = secret
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = (timestamp + request.method + request.path_url + (request.body or '')).encode("utf-8")
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())
        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


def main():
    welcome()
    client = CoinbasePRO()
    print(client.get("products").json())


if __name__ == "__main__":
    main()
