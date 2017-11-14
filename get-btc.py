import gdax
import os

API_KEY = os.environ['GDAX_API_KEY']
API_SECRET = os.environ['GDAX_API_SECRET']
API_PASS = os.environ['GDAX_API_PASS']


def main():
    '''
    Gets the current bitcoin price in usd and prints to the screen.
    '''
    client = gdax.AuthenticatedClient(API_KEY, API_SECRET, API_PASS)
    ticker = client.get_product_ticker(product_id='BTC-USD')
    print(ticker["price"])


if __name__ == '__main__':
    main()
