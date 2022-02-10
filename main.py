import crawler.crawler_histock as histock
import crawler.crawler_yahoo as yahoo
import time

for stock_symbol in ['2330', '0056']:
    yahoo_class = yahoo.yahoo()
    print(yahoo_class.record_closing(stock_symbol))
    print(yahoo_class.record_daily_diff(stock_symbol))
    time.sleep(1)
