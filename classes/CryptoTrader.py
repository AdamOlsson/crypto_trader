import datetime, time, signal

# https://binance-docs.github.io/apidocs/spot/en/

class CryptoTrader():
    
    def __init__(self, strategy, binance_interface, asset, logger=None):
        self.strategy = strategy
        self.binance_interface = binance_interface
        self.logger = logger
        self.asset = asset
        self.engine = CryptoTraderEngine(strategy, binance_interface, logger, asset)

    def run(self):

        asset_balance = self.binance_interface.get_asset_balance(self.asset)
        if asset_balance > 0.0001:
            answer = input(
                "You currently are in a trade of {} {}. Application needs to start on 0 {}. \nWould you like to the application to sell your {} at market price? (yes/no)\n"
                .format(asset_balance, self.asset, self.asset, self.asset))
            if answer == "yes" or answer == "y":
                ack = self.binance_interface.sell(self.asset)
                print("Sell acknowledgement:\n{}".format(ack))
            elif answer == "n" or answer == "n":
                print("You answered 'No', exiting application.") # exit
                exit()
            else:
                print("Invalid answer. Exiting.")
                exit()

        self.engine.run()



class CryptoTraderEngine:
    terminal_status_print_format = "LocalTime {},ServerTime: {},Capital: {}EUR,Earnings from start: {},In trade: {}         "

    def __init__(self, strategy, binance_interface, logger, asset):
        self.strategy = strategy
        self.binance_interface = binance_interface
        self.logger = logger
        self.asset = asset

    def run(self):
        def show_status_terminal(local_time, server_time_s, capital, earnings, in_trade):
            print(self.terminal_status_print_format.format(
                local_time.strftime("%Y-%m-%d %H:%M:%S"),
                datetime.datetime.utcfromtimestamp(server_time_s).strftime('%Y-%m-%d %H:%M:%S'),
                capital,
                earnings,
                in_trade), end="\r")

        self.g_keyboard_interrupt_signal = False
        def sigint_handler(signal, frame):
            print ("\nKeyboard interrupt! Exiting... Please wait for iteration to finish.")
            self.g_keyboard_interrupt_signal = True
        signal.signal(signal.SIGINT, sigint_handler)
        

        while True:

            server_time_s = int(self.binance_interface.get_server_time()/1000) # Binance store server time in milliseconds
            local_time = datetime.datetime.now()

            action = self.strategy.step()

            if action == "BUY":
                ack = self.binance_interface.buy()
            elif action == "SELL":
                ack = self.binance_interface.sell(self.asset)
            else: # action == "HOLD"
                pass # do nothing

            # Logging, Binance returns an empty dict when using the order_test API
            if bool(ack) and (action == "BUY" or action == "SELL"):
                orderId = ack["orderId"]
                order = self.binance_interface.getOrder(orderId)
                self.logger.log(order)

            capital = self.binance_interface.get_capital(self.asset)
            show_status_terminal(
                local_time, server_time_s,
                capital,capital - self.strategy.starting_capital,
                self.strategy.get_in_trade())

            # Always fetch data 10s after full minute
            sleep_time = 69 - local_time.second
            time.sleep(sleep_time)

            if self.g_keyboard_interrupt_signal:
                break