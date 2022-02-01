from bs4 import BeautifulSoup
import requests
import pandas as pd
import itertools
import datetime
import sys
import json
import re
import time
sys.path.append("..")
import database.database as database  # noqa


class yahoo:
    today_date = ''
    today_datetime = ''

    # {Function 建構式}
    def __init__(self):
        self.today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.today_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # {Function 紀錄上市股票漲幅排行}
    # {Return bool 是否紀錄成功}
    def record_change_up() -> bool:
        url = 'https://tw.stock.yahoo.com/rank/change-up?exchange=TAI'
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        change_up_html = soup.select('li.List\(n\) > div')
        # stock_data 預期格式
        # [
        #     [名次, 股名, 股號, 成交價, 漲跌, 漲跌幅, 最高, 最低, 價差, 成交量(張), 成交值(億)],
        #     ['1', '瑞利', '1512.TW', '5.39', '0.49', '10.00%', '5.39', '4.91', '0.48', '753', '0.0397'],
        #     ['2', '業旺', '1475.TW', '56.10', '5.10', '10.00%', '56.10', '52.00', '4.10', '301', '0.1669']
        # ]
        #
        stock_data = []
        times = 1
        for data in change_up_html:
            # stripped_strings 參考資料：https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#get-text
            # TODO: 將股號中的 .tw 移除
            stock_data.append([text for text in data.stripped_strings])
            times += 1
            if times > 10:
                break

    # {Function 紀錄法人買賣總覽}
    # {Return bool 是否紀錄成功}
    def record_qsp_trading_summary(self, stock_symbol: str) -> bool:
        # 取當日資料
        url = 'https://tw.stock.yahoo.com/quote/{}/institutional-trading' \
            .format(stock_symbol)
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        # 取資料時間
        data_time = soup.select('#qsp-trading-summary time')[0]['datatime']
        # 取資料
        # the_day_data 預期格式
        # [
        #     ['外資', '29,198', '14,082', '15,116', '連2買 (23,377)'],
        #     ['投信', '556', '189', '367', '連8買 (8,021)'],
        #     ['自營商', '1,299', '953', '346', '賣→買 (346)'],
        #     ['三大法人', '31,052', '15,224', '15,829', '連3買 (23,844)'],
        # ]
        the_day_html = soup.select('#qsp-trading-summary > div.Pos\(r\) li')
        the_day_data = []
        for personal_data in the_day_html:
            the_day_data.append(
                [
                    text.replace(',', '')
                    for text in personal_data.stripped_strings
                ]
            )

        # 取累積資料(用 api 取)
        url = 'https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.trades;accumulation=true;symbol={}' \
            .format(stock_symbol)
        data = json.loads(requests.get(url).text)
        # api 回傳格式
        # {
        #     "list": [
        #         {
        #             "dealerBuyVolK": 1586,          自營商買進
        #             "dealerDiffVolK": -659,         自營商淨買賣
        #             "dealerSellVolK": 2245,         自營商賣出
        #             "foreignBuyVolK": 55533,        外資買進
        #             "foreignDiffVolK": 23377,       外資淨買賣
        #             "foreignSellVolK": 32156,       外資賣出
        #             "investmentTrustBuyVolK": 1035, 投信買進
        #             "investmentTrustDiffVolK": 627, 投信淨買賣
        #             "investmentTrustSellVolK": 408, 投信賣出
        #             "periodSum": "2D",              統計天數, D:日 M:月 Y:年
        #             "totalBuyVolK": 58153,          三大法人買進
        #             "totalDiffVolK": 23345,         三大法人淨買賣
        #             "totalSellVolK": 34809          三大法人賣出
        #         },
        #         {
        #             ...
        #         }
        #     ],
        #     "refreshedTs": "2022-01-12T00:00:00+08:00" 資料時間
        # }

    # {Function 紀錄收盤價}
    # {Return bool 是否紀錄成功}
    def record_closing(self, stock_symbol: str) -> bool:
        url = 'https://tw.stock.yahoo.com/quote/{}/institutional-trading' \
            .format(stock_symbol)
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        stock_price_html = soup.select('.Fld\(c\).Ai\(fs\) > div')
        performance = 'up' if soup.select(
            '.Fld\(c\).Ai\(fs\) .Ai\(fe\) .C\(\$c-trend-up\)') else 'down'
        loop_times = 0
        data = {}
        for text in stock_price_html[0].stripped_strings:
            # 第一個值是收盤價
            if loop_times == 0:
                data['price'] = text
            # 第二個值是漲跌幅
            elif loop_times == 1:
                data['diff'] = text if performance == 'up' else '-' + text
            # 第三個值是漲跌百分比
            elif loop_times == 2:
                pattern = r"([0]{1}|[1-9]{1}\d*)(\.\d+)%"
                text = re.search(pattern, text)[0]
                data['diff_percent'] = text if performance == 'up' else '-' + text
            loop_times += 1

        # 取收盤時間
        close_date_html = soup.select('.Fld\(c\).Ai\(fs\) > span')
        pattern = r"(\d{4}/\d{2}/\d{2})"
        time_string = re.search(pattern, close_date_html[0].text)[0]
        data['date'] = time.strftime(
            "%Y-%m-%d",
            time.strptime(time_string, "%Y/%m/%d")
        )
