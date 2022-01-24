import crawler.crawler_histock as histock
import time

for stock_symbol in ['2330', '0056']:
    histock_class = histock.histock(stock_symbol)
    print(histock_class.record_performance())
    print(histock_class.record_profit())
    time.sleep(1)

# 下面這個寫法好像也不錯
# 參考資料：https://stackoverflow.com/questions/3679592/python-update-class-instance-to-reflect-change-in-a-class-method
# objs = [histock.histock(stock_symbol) for stock_symbol in ['2330', '0056']]
# for obj in objs:
#     obj.record_performance()
#     time.sleep(1)

# @todo 對付__pycache__的幾種方法(https://tech.gjlmotea.com/2020/03/pythonpycache.html)
# @todo google python import 不同資料夾
