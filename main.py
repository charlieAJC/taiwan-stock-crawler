import crawler.crawler_histock as histock
import crawler.crawler_yahoo as yahoo
import time

for stock_symbol in ['2330', '0056']:
    yahoo_class = yahoo.yahoo()
    print(yahoo_class.record_closing(stock_symbol))
    print(yahoo_class.record_daily_diff(stock_symbol))
    time.sleep(1)

# 下面這個寫法好像也不錯
# 參考資料：https://stackoverflow.com/questions/3679592/python-update-class-instance-to-reflect-change-in-a-class-method
# objs = [histock.histock(stock_symbol) for stock_symbol in ['2330', '0056']]
# for obj in objs:
#     obj.record_performance()
#     time.sleep(1)

# @todo 對付__pycache__的幾種方法(https://tech.gjlmotea.com/2020/03/pythonpycache.html)
# @todo google python import 不同資料夾
