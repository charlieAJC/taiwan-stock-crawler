from bs4 import BeautifulSoup
import requests
import pandas as pd
import itertools
import datetime
import sys
sys.path.append("..")
import database.database as database  # noqa


# 爬蟲取得 histock 個股資訊
class histock:
    histock_url = "https://histock.tw/stock/{}"
    # 股票代號
    stock_symbol = ''
    soup = ''
    today_date = ''
    today_datetime = ''

    # {Function 建構式}
    # {Input stock_symbol {string} 股票代號}
    def __init__(self, stock_symbol: str):
        self.stock_symbol = stock_symbol
        self.histock_url = self.histock_url.format(self.stock_symbol)
        self.soup = BeautifulSoup(requests.get(self.histock_url).text, 'lxml')
        self.today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.today_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # {Function 紀錄大盤和各股的近期表現}
    # {Return bool 是否紀錄成功}
    def record_performance(self) -> bool:
        html_table = str(self.soup.select('table.tb-stock.tbPerform')[0])
        pandas_table = pd.read_html(html_table)
        # 取得個股的近期表現
        single_data = pandas_table[0].iloc[:, 1].tolist()
        # 取得大盤的近期表現
        market_data = pandas_table[0].iloc[:, 2].tolist()

        single_string = ','.join(
            [f"{c.replace('%', '')}" for c in single_data])
        market_string = ','.join(
            [f"{c.replace('%', '')}" for c in market_data])
        # 使用 INSERT ... ON DUPLICATE KEY UPDATE 避免資料重複更新
        # 大盤股票代號設定為 0
        sql = f"INSERT INTO `stock_performance` VALUES " + \
            f"(null,'0','{self.today_date}',{market_string},'{self.today_datetime}','{self.today_datetime}')," + \
            f"(null,'{self.stock_symbol}','{self.today_date}',{single_string},'{self.today_datetime}','{self.today_datetime}') " + \
            f"ON DUPLICATE KEY UPDATE id=id"
        result = database.run_sql(sql)
        if (result == False):
            return False
        else:
            return True

    # {Function 紀錄券商分點績效/獲利分析}
    # {Return bool 是否紀錄成功}
    def record_profit(self) -> bool:
        html_table = str(self.soup.select('table.tbTable.tb-stock.tbChip')[0])
        pandas_table = pd.read_html(html_table)
        profit_table = pandas_table[0].iloc[:, 1:].values.tolist()

        order = 1
        sql = 'INSERT INTO `main_profit` VALUES '
        count = len(profit_table)
        for profit in profit_table:
            sql += f"(null,'{self.stock_symbol}','{self.today_date}',{order}," + \
                f"'{profit[0]}',{profit[1].replace('%', '')},{profit[2]},{profit[3]},{profit[4]}," + \
                f"'{self.today_datetime}','{self.today_datetime}')"
            if order < count:
                sql += ','
            order += 1
        result = database.run_sql(sql)
        if (result == False):
            return False
        else:
            return True
