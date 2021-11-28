import datetime, time, sys, signal

class CryptoTrader():
    terminal_status_print_format = "LocalTime {},ServerTime: {},Capital: {}EUR,Earnings from start: {},In trade: {}"
    
    def __init__(self, strategy, api):
        self.strategy = strategy
        self.api = api

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

        # TODO: Fetch initial status (in trade or not) for when a restart is needed.

        while True:
            data = self.api.get()
            server_time_s = int(self.api.get_server_time()/1000)
            local_time = datetime.datetime.now()

            capital = self.strategy.step(data)
            # TODO: Implement an emergency exit

            show_status_terminal(
                local_time, server_time_s,
                capital,capital - self.strategy.starting_capital,
                self.strategy.get_in_trade())

            # Always fetch data 10s after full minute
            sleep_time = 69 - local_time.second
            time.sleep(sleep_time)
            # time.sleep(5)

            if self.g_keyboard_interrupt_signal:
                break
