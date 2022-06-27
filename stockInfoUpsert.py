import requests
from lxml import etree
import json
import numpy as np

def stockInfo(url):
    res = requests.get(url)
    content = res.text
    html = etree.HTML(content)
    oldColumnName = html.xpath('//tr[1]//text()')
    NewColumnName = ['marketType', 'ticker', 'name'] + oldColumnName[1:]

    resultList = []
    for tr in html.xpath('//tr')[1:]:
        if tr.xpath('td/b/text()'):
            tmpMarketType = tr.xpath('td/b/text()')[0]
        else:
            nameCode = tr.xpath('td[1]/text()')[0].split('\u3000')
            tmpRow = [tr.xpath(f'td[{i}]/text()')[0] if tr.xpath(f'td[{i}]/text()') else np.nan for i in range(2, len(oldColumnName)+1) ]
            tmpDict = dict(zip(NewColumnName, [tmpMarketType] + nameCode + tmpRow))
            resultList.append(tmpDict) 
    return resultList

List = stockInfo("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
result = [{"ticker":i["ticker"], "name": i["name"], "listed_at":i["上市日"], "industry":i['產業別']} for i in List if i['marketType'] == ' 股票 ']

with open("listed.json","w") as file: 
    json.dump(result,file, ensure_ascii = False)

# print('result: ', result, 'len(result)', len(result))
