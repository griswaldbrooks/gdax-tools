import gdax
import os
import json

API_KEY = os.environ['GDAX_API_KEY']
API_SECRET = os.environ['GDAX_API_SECRET']
API_PASS = os.environ['GDAX_API_PASS']
USD_ID = os.environ['GDAX_USD_ID']


def main():
    '''
    Puts in a limit order at a specified price using all funds.
    '''
    client = gdax.AuthenticatedClient(API_KEY, API_SECRET, API_PASS)
    r = client.get_account(USD_ID)
    print(json.dumps(r))


if __name__ == '__main__':
    main()
