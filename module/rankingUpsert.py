import json
import requests
import datetime, time 
import traceback
import numpy as np
import pandas as pd 

class Ranking():
    def __init__(self, industrySort, dateTime):
        self.dateTime = dateTime
        self.lastMonth = self.dateTime + datetime.timedelta(days = -20)
        self.industrySort = industrySort
        self.result = []
        self.rankingResult = []
        
    def _requestsUtil(self, dateTime, ticker, retry = 1):
        try:
            url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date={}&stockNo={}".format(dateTime.strftime("%Y%m%d"), ticker)
            time.sleep(3)
            res = requests.get(url).text
            if 'html' in res:
                print("回應存在'html'資料: ", ticker)
                time.sleep(10)
                return self._requestsUtil(dateTime, ticker)
            else:
                res = json.loads(res)
                if res['stat'] == "OK" and res['data'] and res['fields'] :
                    return res
                elif retry:
                    
                    return self._requestsUtil(dateTime, ticker, retry = retry - 1)
                else:
                    print("[API資料不完整]", {'ticker':ticker,"url": url, "response: ": res} )
                    return False
        except Exception as e:
            traceback.print_exc()

    def _returnCal(self, ticker, res):
        """
            data =  [
                [ "111/06/01", "29,502,561", "15,790,689,728", "538.00", "540.00", "530.00", "531.00", "-7.00", "48,050"],
                [ "111/06/02", "863,623", "1,368,479,900", "1,540.00", "1,630.00", "1,525.00", "1,620.00", "+55.00", "2,798"],
                [ "111/06/03", "21,163", "1,033,447", "45.00", "49.50", "45.00", "48.65", "X0.00", "34"]
            ]
        """
        try:
            data = res['data']
            dataExtract = [i for i in  data if i[0] == '{}/{}/{}'.format(self.dateTime.year-1911, self.dateTime.strftime("%m"), self.dateTime.strftime("%d"))]
            if dataExtract :
                if "--" in (dataExtract[0][-2], dataExtract[0][-3]) or "X0.00" in (dataExtract[0][-2], dataExtract[0][-3]):
                    print("[存在'--'或'X0.00'資料]: ", ticker)
                    return self._missDataProcess(ticker, res)
                else:
                    close = float(dataExtract[0][-3].replace(",", ""))
                    todayDiff = float(dataExtract[0][-2].replace(",", ""))
                    yesterdayClose = close - todayDiff
                    diff = todayDiff / yesterdayClose
                    return {"ticker": ticker, "diff": diff}
            else:
                print('[API資料不完整]', ticker)
                return False
        except Exception as e:
            traceback.print_exc()
            
    def _missDataProcess(self, ticker, res):
        try:
            if len(res['data']) > 1:
                return self._dataFrameUtil(ticker, res['data'], res['fields'])
            elif len(res['data']) == 1:
                lastMonthRes = self._requestsUtil(self.lastMonth, ticker)
                if lastMonthRes:
                    return self._dataFrameUtil(ticker, lastMonthRes['data'] + res['data'], res['fields'])
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
                diff = Df.loc['{}/{}/{}'.format(self.dateTime.year-1911, self.dateTime.strftime("%m"), self.dateTime.strftime("%d")), '收盤漲幅']
            else:
                Df['收盤價'] = [float(i.replace(",", "")) for i in Df['收盤價'].tolist()]
                Df['收盤漲幅'] = Df['收盤價'].astype('float').pct_change()
                diff = Df.loc['{}/{}/{}'.format(self.dateTime.year-1911, self.dateTime.strftime("%m"), self.dateTime.strftime("%d")), '收盤漲幅']
            if (diff or diff == 0.0) and ~np.isnan(diff):
                return {"ticker": ticker, "diff": diff}
            else:
                print('[API資料不完整]', {"ticker": ticker, "diff": diff})
                return False
        except Exception as e:
            traceback.print_exc()
            
    def _setRanking(self, industry, tmpList):
        try:
            sortListofDict = sorted(tmpList, key=lambda k: k['diff'], reverse=True)[0:3]
            finalResult = [{"ticker" : i["ticker"], "diff":"{:.2f}%".format(i["diff"] * 100)} for i in sortListofDict]
            self.rankingResult.append({'industry' : industry, 'result': finalResult})
            print("-----------------RANKING  RESULT-----------------")
            print(f' [{self.dateTime}_{industry}]','\n', finalResult)
            print("---------------------CLOSE-----------------------")   
        except Exception as e:
            traceback.print_exc()

    def rankExtract(self):
        try:
            for industry, vals in self.industrySort.items():
                tmpList = []
                print('[INDUSTRY]: ', industry)
                for val in vals:
                    ticker = val['ticker']
                    result = False
                    res = self._requestsUtil(self.dateTime, ticker)
                    if res: 
                        result = self._returnCal(ticker, res)
                        if result:
                            print(result)
                            tmpList.append(result)
                print("-----------------ALL  RESULT-----------------")
                print(tmpList)
                self.result.append({'industry' : industry, 'result': tmpList})
                self._setRanking(industry, tmpList)
        except Exception as e:
            traceback.print_exc()