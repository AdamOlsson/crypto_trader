from datetime import datetime
import json

class Logger():
    log_header = "#LocalTime,OpenTime,Action,Price,AmountCrypto,AmountEUR"
    log_format = ("{},"*len(log_header.split(",")))[0:-1]

    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.log_file = self.log_dir + "/log.csv"

    def log(self, order):
        with open(self.log_file, "a") as f:
            f.write(json.dumps(order) + "\n")
