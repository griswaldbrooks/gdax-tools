import gdax
import os
import time
import numpy as np

API_KEY = os.environ["GDAX_API_KEY"]
API_SECRET = os.environ["GDAX_API_SECRET"]
API_PASS = os.environ["GDAX_API_PASS"]


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class wsClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        self.previous_trade = 0
        self.buy_price = 8269.00
        self.sell_price = 0
        self.history = np.zeros(100)
        self.usd = 2550.00
        self.btc = 0.0

    def on_message(self, msg):
        if "price" in msg and "type" in msg:
            if msg["type"] == "match":
                # Convert from string.
                trade_price = float(msg["price"])

                # Check for initialization.
                if self.previous_trade == 0:
                    self.previous_trade = trade_price
                    self.history.fill(trade_price)
                    return

                # Compute statistics.
                price_change = trade_price - self.previous_trade
                percent_change = price_change / trade_price
                buy_percent = (trade_price - self.buy_price) / self.buy_price

                buy_thresh = 1.003 * self.sell_price
                sell_thresh = 0.997 * self.buy_price
                # Buy
                if self.usd != 0 and trade_price > buy_thresh:
                    print("Buy")
                    self.buy_price = trade_price
                    self.btc = (self.usd / trade_price) * 0.997
                    self.usd = 0
                # Sell
                elif self.btc != 0 and trade_price < sell_thresh:
                    print("Sell")
                    self.sell_price = trade_price
                    self.usd = (self.btc * trade_price) * 0.997
                    self.btc = 0

                # Format and print to terminal.
                color = bcolors.BOLD
                if price_change < 0:
                    color = bcolors.FAIL
                elif price_change > 0:
                    color = bcolors.OKGREEN

                price_change_s = "${:.3f}".format(price_change)
                percent_change_s = "{:.5f}%".format(percent_change * 100)
                buy_percent_s = "{:.5f}%".format(buy_percent * 100)
                print(color + "${:.3f} {} {} {} ${} BTC{} ${} ${} ${}".format(
                    trade_price,
                    price_change_s,
                    percent_change_s,
                    buy_percent_s,
                    self.usd,
                    self.btc,
                    buy_thresh,
                    sell_thresh,
                    trade_price * self.btc) + bcolors.ENDC)

                # Update state.
                self.previous_trade = trade_price
                self.history = np.append(self.history, trade_price)
                self.history = np.delete(self.history, 0)

    def on_close(self):
        print("-- Goodbye! --")


def main():
    '''
    Displays graph of BTC-USD price.
    '''
    try:
        # Set up gdax websocket.
        client = wsClient()
        client.start()

        # Run loop.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()

    except Exception as e:
        print(e)
        client.close()


if __name__ == '__main__':
    main()
