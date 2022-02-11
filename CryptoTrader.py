import datetime, time, sys, signal

class CryptoTrader():
    terminal_status_print_format = "LocalTime {},ServerTime: {},Capital: {}EUR,Earnings from start: {},In trade: {}"
    
    def __init__(self, strategy, binance_interface, logger=None):
        self.strategy = strategy
        self.binance_interface = binance_interface
        self.logger = logger

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
            try: # try-catch clause for stub
                kline_data = self.binance_interface.get()
            except IndexError:
                break
        
            server_time_s = int(self.binance_interface.get_server_time()/1000)
            local_time = datetime.datetime.now()

            action = self.strategy.step(kline_data)
            # TODO: Implement an emergency exit

            if action == "BUY":
                self.binance_interface.buy()
            elif action == "SELL":
                self.binance_interface.sell()
            else: #"HOLD"
                pass # do nothing

            capital = self.binance_interface.get_capital()
            show_status_terminal(
                local_time, server_time_s,
                capital,capital - self.strategy.starting_capital,
                self.strategy.get_in_trade())

            # TODO: Move this wait to some kind of engine
            # Always fetch data 10s after full minute
            sleep_time = 69 - local_time.second
            #time.sleep(sleep_time)

            if self.g_keyboard_interrupt_signal:
                break
