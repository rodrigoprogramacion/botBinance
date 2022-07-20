from binance.cm_futures import CMFutures
import config as c

cm_futures_client = CMFutures (key=c.API_KEY, secret=c.SECRET_KEY)
b=cm_futures_client.balance()
print("Balance: ", b)