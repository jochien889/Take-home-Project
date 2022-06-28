import requests
from lxml import etree
import json
import numpy as np
import traceback

class StockList():
    def __init__(self, path = 'result/', isSave = True):
        self.path = path
        self.isSave = isSave
        self.resultList = []
        
    def stockListExtract(self):
        try:
            res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
            content = res.text
            html = etree.HTML(content)
            oldColumnName = html.xpath('//tr[1]//text()')
            NewColumnName = ['marketType', 'ticker', 'name'] + oldColumnName[1:]

            for tr in html.xpath('//tr')[1:]:
                if tr.xpath('td/b/text()'):
                    tmpMarketType = tr.xpath('td/b/text()')[0]
                else:
                    nameCode = tr.xpath('td[1]/text()')[0].split('\u3000')
                    tmpRow = [tr.xpath(f'td[{i}]/text()')[0] if tr.xpath(f'td[{i}]/text()') else np.nan for i in range(2, len(oldColumnName)+1) ]
                    tmpDict = dict(zip(NewColumnName, [tmpMarketType] + nameCode + tmpRow))
                    self.resultList.append(tmpDict) 
            self._dataTransform()
        except Exception as e:
            traceback.print_exc()
            
    def _dataTransform(self): 
        self.finalResultList = [{"ticker":i["ticker"], "name": i["name"], "listed_at":i["上市日"], "industry":i['產業別']} for i in self.resultList if i['marketType'] == ' 股票 ']
        if self.isSave:
            with open( self.path + "listed.json","w", encoding="utf8") as file: 
                json.dump(self.finalResultList , file, ensure_ascii = False)


