import gdax
import os

API_KEY = os.environ["GDAX_API_KEY"]
API_SECRET = os.environ["GDAX_API_SECRET"]
API_PASS = os.environ["GDAX_API_PASS"]


def main():
    '''
    Displays current gdax arbitrage.
    '''

    client = gdax.AuthenticatedClient(API_KEY, API_SECRET, API_PASS)
    btc_usd = float(client.get_product_ticker(product_id='BTC-USD')["price"])
    ltc_btc = float(client.get_product_ticker(product_id='LTC-BTC')["price"])
    ltc_usd = float(client.get_product_ticker(product_id='LTC-USD')["price"])
    eth_btc = float(client.get_product_ticker(product_id='ETH-BTC')["price"])
    eth_usd = float(client.get_product_ticker(product_id='ETH-USD')["price"])
    ltc_btc_usd = ltc_btc * btc_usd
    ltc_btc_arb = (ltc_usd / ltc_btc_usd - 1) * 100
    eth_btc_usd = eth_btc * btc_usd
    eth_btc_arb = (eth_usd / eth_btc_usd - 1) * 100
    print("=" * 100)
    print("LTC-BTC: ${} ${} {:.5f}%".format(ltc_usd, ltc_btc_usd, ltc_btc_arb))
    print("ETH-BTC: ${} ${} {:.5f}%".format(eth_usd, eth_btc_usd, eth_btc_arb))

if __name__ == '__main__':
    main()
