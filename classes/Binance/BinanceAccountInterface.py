from binance.spot import Spot

class BinanceAccountInterface:
    def __init__(self, spot):
        self.spot = spot

    def buy(self):
        symbol = "BTCEUR"
        side = "BUY"
        type = "LIMIT"
        ack = self.spot.new_order_test(symbol, side, type)
        return ack

    def buy(self):
        symbol = "BTCEUR"
        side = "SELL"
        type = "LIMIT"
        ack = self.spot.new_order_test(symbol, side, type)
        return ack


class BinanceAccountInterfaceStub:
    maker_fee = taker_fee = 1/(100 * 10) # 0.1%

    def __init__(self, binance_interface_stub):
        self.binance_interface_stub = binance_interface_stub

    def compute_fee(self, amount):
        return amount*self.maker_fee

    def buy(self):
        
        price = self.binance_interface_stub.get_current()["Open"]
        fee_eur = self.compute_fee(self.capital)
        crypto = (self.capital - fee_eur)/price

        self.binance_interface_stub.update("BTC", crypto)
        self.binance_interface_stub.update("EUR", 0)

        return {}

    def sell(self, datapoint):
        def compute_earning_from_prev_sell():
            return self.return_from_sell - self.capital_before_buy

        price = self.binance_interface_stub.get_current()["Open"]

        value_eur = price*self.crypto
        self.capital = value_eur - self.compute_fee(value_eur)

        self.crypto = 0

        return {}