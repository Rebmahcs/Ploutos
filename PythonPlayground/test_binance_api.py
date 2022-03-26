import time

from dotenv import dotenv_values
from binance.client import Client


# If you have issue on windows ( Timestamp ahead ) look at the last answer
# https://github.com/sammchardy/python-binance/issues/249

def welcome():
    print('Starting Ploutos project - Binance version. \n')



def init_binance_client(test_mode=False):
    API_KEY_CONF = "API_KEY"
    API_SECRET_CONF = "API_SECRET"

    binance_conf = dotenv_values('.env.binance.test' if test_mode else '.env.binance')
    client = Client(binance_conf[API_KEY_CONF], binance_conf[API_SECRET_CONF])

    if test_mode:
        client.API_URL = 'https://testnet.binance.vision/api'

    return client


def main():
    welcome()
    client = init_binance_client(True)
    print(client.get_account())

if __name__ == '__main__':
    main()
