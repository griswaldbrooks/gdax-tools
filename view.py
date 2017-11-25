import gdax
import os
import time
import matplotlib.pyplot as plt
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
        self.buy_price = 8464.99
        self.history = np.zeros(100)

    def on_message(self, msg):
        if "price" in msg and "type" in msg:
            if msg["type"] == "match":
                # Convert from string.
                trade_price = float(msg["price"])

                # Check for initialization.
                if self.previous_trade == 0:
                    self.previous_trade = trade_price
                    self.history.fill(trade_price)

                # Compute statistics.
                price_change = trade_price - self.previous_trade
                percent_change = price_change / trade_price
                buy_percent = (trade_price - self.buy_price) / self.buy_price

                # Format and print to terminal.
                color = bcolors.BOLD
                if price_change < 0:
                    color = bcolors.FAIL
                elif price_change > 0:
                    color = bcolors.OKGREEN

                price_change_s = "${:.3f}".format(price_change)
                percent_change_s = "{:.5f}%".format(percent_change * 100)
                buy_percent_s = "{:.5f}%".format(buy_percent * 100)
                print(color + "{} ${:.3f} {} {} {}".format(
                    time.time(),
                    trade_price,
                    price_change_s,
                    percent_change_s,
                    buy_percent_s) + bcolors.ENDC)

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

        # Set up plots.
        plt.ion()
        Y_MARGIN = 0.1
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.axhline(y=0, color="r", linestyle="--")
        line, = ax.plot(client.history)
        txt_x = 0
        txt_y = 0
#        gain_label = ax.text(txt_x, txt_y, "Current Gain")
        gain_text = ax.text(txt_x + 40, txt_y, "")
#        gain_label.set_size(48)
        gain_text.set_size(48)
        ax.set_ylim(-0.1, 2)
        ax.set_ylabel("Percent Gain")
        ax.set_xlabel("Trade History")

        # Run loop.
        while True:
            pt = (client.history / client.buy_price - 1) * 100
            percent_change = pt[-1]
            # Ensure we can see the graph.
            p_min = min(pt)
            p_max = max(pt)
            ax.set_ylim(p_min - Y_MARGIN, p_max + Y_MARGIN)

            percent_change_s = "{:.5f}%".format(percent_change)

            line.set_ydata(pt)
#           gain_label.set_y(percent_change - Y_MARGIN * 0.95)
            gain_text.set_y(percent_change - Y_MARGIN * 0.95)
            gain_text.set_text(percent_change_s)
            fig.canvas.draw()
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()

    except Exception as e:
        print(e)
        client.close()


if __name__ == '__main__':
    main()
