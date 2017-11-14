import gdax
import os
import json
import argparse

API_KEY = os.environ['GDAX_API_KEY']
API_SECRET = os.environ['GDAX_API_SECRET']
API_PASS = os.environ['GDAX_API_PASS']
USD_ID = os.environ['GDAX_USD_ID']


def main():
    '''
    Puts in a limit order at a specified price using all funds.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('ask',   type=float,                         help='Asking price for order in USD.')
    parser.add_argument('--usd', type=float, default=-1.0,           help='Amount of dollars to use.')
    parser.add_argument('--btc', type=float, default=-1.0,           help='Amount of bitcoin to ask.')
    parser.add_argument('--all', action='store_true', default=False, help='Buy using all USD in account.')
    args = parser.parse_args()
    print(args)

    # Only one argument should be used. If more than one is specified, abort.
    if sum([args.all, args.usd >= 0, args.btc >= 0]) > 1:
        print("Only amount to buy or all should be specified.")
        return

    client = gdax.AuthenticatedClient(API_KEY, API_SECRET, API_PASS)
    r = client.get_account(USD_ID)
    print(json.dumps(r))


if __name__ == '__main__':
    main()
