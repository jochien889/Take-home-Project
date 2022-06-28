from fake_useragent import UserAgent
import json
import requests
import datetime, time 
import traceback
import numpy as np
import pandas as pd 

class Ranking():
    def __init__(self, industrySort, dateTime, path = 'result/', isSave = True):
        self.dateTime = dateTime
        self.lastMonth = self.dateTime + datetime.timedelta(days = -20)
        self.path = path
        self.isSave = isSave
        self.industrySort = industrySort
        self.result = []
        self.rankingResult = []
        
    def _requestsUtil(self, dateTime, ticker, retry = 1):
        try:
            url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date={}&stockNo={}".format(self.dateTime.strftime("%Y%m%d"), ticker)
            time.sleep(3)
            res = requests.get(url).text
            if 'html' in res:
                print(f'[WEB_ERROR_{ticker}]')
                time.sleep(10)
                return self._requestsUtil(dateTime, ticker)
            else:
                res = json.loads(res)
                if res['stat'] == "OK" and res['data'] and res['fields'] :
                    return res
                elif retry:
                    
                    return self._requestsUtil(dateTime, ticker, retry = retry - 1)
                else:
                    print("{}資料不存在".format(ticker), ", url: ", url, "response: ", res)
                    return False
        except Exception as e:
            traceback.print_exc()

    def _dataFrameUtil(self, ticker, dataList, columnList):
        """["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]"""
        try:
            Df = pd.DataFrame(dataList, columns = columnList)
            Df.set_index("日期" , inplace=True)
            if '--' in Df['收盤價'].tolist():
                Df['收盤價'] = [i.replace(",", "") for i in Df['收盤價']]
                Df = Df.replace('--', np.nan)
                Df['收盤價'] = Df['收盤價'].astype('float')
                Df['shift'] = Df['收盤價'].shift()
                Df['收盤漲幅'] = (Df['收盤價'] - Df['shift'])/Df['shift']
                diff = Df.loc['{}/{}/{}'.format(self.dateTime.year-1911, self.dateTime.strftime("%m"), self.dateTime.day), '收盤漲幅']
            else:
                Df['收盤價'] = [float(i.replace(",", "")) for i in Df['收盤價'].tolist()]
                Df['收盤漲幅'] = Df['收盤價'].astype('float').pct_change()
                diff = Df.loc['{}/{}/{}'.format(self.dateTime.year-1911, self.dateTime.strftime("%m"), self.dateTime.day), '收盤漲幅']

            if (diff or diff == 0.0) and ~np.isnan(diff):
                return {"ticker": ticker, "diff": diff}
            else:
                print('[ERROR]', {"ticker": ticker, "diff": diff})
                return False
        except Exception as e:
            traceback.print_exc()

    def _listedFirstDay(self, ticker, data):
        """["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]"""
        try:
            diff = data[-2].replace(",", "")/(data[-3].replace(",", "") - data[-2].replace(",", ""))
            if type(diff) == float:
                return {"ticker": ticker, "diff": diff}
            else:
                print('[ERROR]', {"ticker": ticker, "diff": diff})
                return False
        except Exception as e:
            traceback.print_exc()

    def _setRanking(self, industry, tmpList):
        sortListofDict = sorted(tmpList, key=lambda k: k['diff'], reverse=True)[0:3]
        finalResult = [{"ticker" : i["ticker"], "diff":"{:.2f}%".format(i["diff"] * 100)} for i in sortListofDict]
        self.rankingResult.append({'industry' : industry, 'result': finalResult})
        print("-----------------RESULT-----------------")
        print(f' [{self.dateTime}_{industry}]','\n', finalResult)
        print("----------------------------------------")   
        if self.isSave:     
            with open(self.path + "{}_top3.json".format(industry), 'w') as File:
                json.dump(finalResult, File, ensure_ascii = False)

    def rankExtract(self):
        for industry, vals in self.industrySort.items():
            tmpList = []
            print('[industry]: ', industry)
            for val in vals:
                ticker = val['ticker']
                listed_at = val['listed_at']
                result = False
                thisMonthRes = self._requestsUtil(self.dateTime, ticker)
                if thisMonthRes: 
                    if len(thisMonthRes['data']) > 1 :
                        """"有歷史資料可以計算"""
                        result = self._dataFrameUtil( ticker, thisMonthRes['data'], thisMonthRes['fields'])
                        if result:
                            print("[RESULT_1]",result)
                            tmpList.append(result)

                    elif len(thisMonthRes['data']) == 1  and  listed_at !=  self.dateTime.strftime("%Y/%m/%d"):
                        """前日收盤價為上個月"""
                        lastMonthRes = self._requestsUtil(self.lastMonth, ticker)
                        result = self._dataFrameUtil(ticker, lastMonthRes['data'] + thisMonthRes['data'], thisMonthRes['fields'])
                        if result:
                            print("[RESULT_2]",result)
                            tmpList.append(result)     

                    elif listed_at ==  self.dateTime.strftime("%Y/%m/%d") and '{}/{}/{}'.format(self.dateTime.year-1911, self.dateTime.strftime("%m"), self.dateTime.day) == thisMonthRes['data'][0][0]:
                        """股票首次上市"""
                        data = thisMonthRes['data'][0]
                        result = self._listedFirstDay(ticker, data)
                        if result:
                            print("[RESULT_2]",result)
                            tmpList.append(result)
                    else:
                        print("資料不存在")
                else:
                    print(f'[ERROR_{ticker}]', thisMonthRes)
            print('[CHECKPOINT]', tmpList)
            self.result.append({'industry' : industry, 'result': tmpList})
            self._setRanking(industry, tmpList)
