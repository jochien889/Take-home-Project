import requests
from lxml import etree
import json
import numpy as np
import traceback
        
def stockListExtract():
    try:
        res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
        content = res.text
        print('content: ', content)
        html = etree.HTML(content)
        oldColumnName = html.xpath('//tr[1]//text()')
        NewColumnName = ['marketType', 'ticker', 'name'] + oldColumnName[1:]
        result = []

        for tr in html.xpath('//tr')[1:]:
            if tr.xpath('td/b/text()'):
                tmpMarketType = tr.xpath('td/b/text()')[0]
            else:
                nameCode = tr.xpath('td[1]/text()')[0].split('\u3000')
                tmpRow = [tr.xpath(f'td[{i}]/text()')[0] if tr.xpath(f'td[{i}]/text()') else np.nan for i in range(2, len(oldColumnName)+1) ]
                tmpDict = dict(zip(NewColumnName, [tmpMarketType] + nameCode + tmpRow))
                result.append(tmpDict) 
        return result
    except Exception as e:
        traceback.print_exc()


