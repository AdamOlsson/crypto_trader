from datetime import datetime
import time

class Logger():
    log_header = "#LocalTime,OpenTime,Action,Price,AmountCrypto,AmountEUR"
    log_format = ("{},"*len(log_header.split(",")))[0:-1]

    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.log_file = self.log_dir + "/log.csv"
        with open(self.log_file, "a") as f:
            f.write(self.log_header + "\n")


    def _log(self, open_time_ms, action, price, amount_crypto, amount_eur):
        local_datetime  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        server_datetime = datetime.utcfromtimestamp(open_time_ms/1000).strftime('%Y-%m-%d %H:%M:%S')

        with open(self.log_file, "a") as f:
            f.write(self.log_format.format(local_datetime, server_datetime, action, price, amount_crypto, amount_eur)+"\n")

    def log_buy(self, datapoint, amount_crypto):
        self._log(datapoint["Open time"], "BUY", datapoint["Open"], amount_crypto, 0)

    def log_sell(self, datapoint, amount_eur):
        self._log(datapoint["Open time"], "SELL", datapoint["Open"], 0, amount_eur)



if __name__ == '__main__':
    datapoint = {"Open time":000000, "Open":66666}
    amount = 0.5
    logger = Logger("./logs")
    logger.log_buy(datapoint, amount)