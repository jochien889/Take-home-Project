from module.stockListUpsert import stockListExtract
import json, requests

if __name__=='__main__':
    res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    content = res.text

    result = stockListExtract(content)
    extractResult = [{"ticker":i["ticker"], "name": i["name"], "listed_at":i["上市日"], "industry":i['產業別']} for i in result if i['marketType'] == ' 股票 ']
    
    with open("result/listed.json","w", encoding="utf8") as file: 
        json.dump(extractResult , file, ensure_ascii = False)
    print('resultList: ', len(result))
    print('finalResultList: ', len(extractResult))