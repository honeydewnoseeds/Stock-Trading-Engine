import threading
import random
import heapq

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type  # 'Buy' or 'Sell'
        self.ticker = ticker  # 1 to 1024
        self.quantity = quantity
        self.price = price
    
    def __lt__(self, other):
        # Buy orders should be sorted in descending order of price
        if self.order_type == 'Buy' and other.order_type == 'Buy':
            return self.price > other.price
        # Sell orders should be sorted in ascending order of price
        if self.order_type == 'Sell' and other.order_type == 'Sell':
            return self.price < other.price
        return self.ticker < other.ticker  # Orders are sorted based on ticker symbol

    def __repr__(self):
        return f"Order({self.order_type}, {self.ticker}, {self.quantity}, {self.price})"
    
class StockExchange:
    def __init__(self):
        self.buy_orders = []  # Min-heap for Buy orders based on ticker
        self.sell_orders = []  # Min-heap for Sell orders based on ticker
    
    def addOrder(self, order_type, ticker, quantity, price):
        order = Order(order_type, ticker, quantity, price)
        
        if order_type == 'Buy':
            heapq.heappush(self.buy_orders, order)
        else:
            heapq.heappush(self.sell_orders, order)
    
    def matchOrder(self):
        while self.buy_orders and self.sell_orders:
            buy_order = heapq.heappop(self.buy_orders)
            sell_order = heapq.heappop(self.sell_orders)
            while buy_order and sell_order:
                if buy_order.ticker == sell_order.ticker:
                    if buy_order.price >= sell_order.price:
                        trade_qty = min(buy_order.quantity, sell_order.quantity)
                        print(f"Trade Executed: {trade_qty} shares of {buy_order.ticker} at price {sell_order.price}")
                        
                        buy_order.quantity -= trade_qty
                        sell_order.quantity -= trade_qty
                        
                        if buy_order.quantity == 0:
                            buy_order = heapq.heappop(self.buy_orders) if self.buy_orders else None
                        if sell_order.quantity == 0:
                            sell_order = heapq.heappop(self.sell_orders) if self.sell_orders else None
                    else:
                        break
                else:
                    if buy_order.ticker < sell_order.ticker:
                        buy_order = heapq.heappop(self.buy_orders) if self.buy_orders else None
                    else:
                        sell_order = heapq.heappop(self.sell_orders) if self.sell_orders else None

# Simulating stock transactions
def simulate_trading(exchange, num_transactions=100):
    # initializing tickers in the range of 1 to 1024
    tickers = [f'TIRK{i}' for i in range(1024)]
    # create random orders
    for _ in range(num_transactions):
        order_type = random.choice(['Buy', 'Sell'])
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = random.uniform(10, 500)
        exchange.addOrder(order_type, ticker, quantity, round(price, 2))
    exchange.matchOrder()

if __name__ == "__main__":
    exchange = StockExchange()
    num_threads = 5 # assuming we only have 5 threads available to run
    threads = []
    
    # running a multi-threading environment
    for _ in range(num_threads):
        t = threading.Thread(target=simulate_trading, args=(exchange, 50))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    