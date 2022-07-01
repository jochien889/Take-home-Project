import requests_mock
from module.rankingUpdate import Ranking
import datetime

def test_standard():
    text1101 = '{"stat":"OK","date":"20220630","title":"111年06月 1101 台泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/29","15,763,786","623,264,030","39.70","39.80","39.40","39.55","-0.05","6,192"],["111/06/30","21,627,885","854,349,929","39.70","39.75","39.25","39.50","-0.05","7,158"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    text1102 = '{"stat":"OK","date":"20220630","title":"111年06月 1102 亞泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/29","3,501,258","153,185,252","4,350","4,395","4,350","4,370","+5","2,159"],["111/06/30","6,623,433","289,927,304","4,395","4,415","4,350","4,380","+10","2,462"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    text1103 = '{"stat":"OK","date":"20220630","title":"111年06月 1103 嘉泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/29","152,262","2,747,807","17.95","18.25","17.95","18.05","-0.25","152"],["111/06/30","519,734","9,295,434","17.95","18.10","17.75","18.10","X0.00","332"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    text1104 = '{"stat":"OK","date":"20220630","title":"111年06月 1104 環泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/29","274,838","6,050,601","21.95","22.10","21.90","22.00","-0.05","221"],["111/06/30","789,493","17,283,194","--","--","--","--","X0.00","412"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    text1108 = '{"stat":"OK","date":"20220630","title":"111年06月 1108 幸福             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/29","47,002","507,420","10.80","10.85","10.75","10.80","-0.10","30"],["111/06/30","181,093","1,933,283","10.75","10.80","10.60","10.70","-0.10","95"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    with requests_mock.mock() as m:
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220630&stockNo=1101",
            text = text1101,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220630&stockNo=1102",
            text = text1102,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220630&stockNo=1103",
            text = text1103,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220630&stockNo=1104",
            text = text1104,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220630&stockNo=1108",
            text = text1108,
        )
        industrySort = {'水泥工業': [{'ticker': '1101', 'listed_at': '1962/02/09'}, {'ticker': '1102', 'listed_at': '1962/06/08'}, {'ticker': '1103', 'listed_at': '1969/11/14'}, {'ticker': '1104', 'listed_at': '1971/02/01'}, {'ticker': '1108', 'listed_at': '1990/06/06'}]}
        dateTime = datetime.datetime(2022, 6, 30)
        exe = Ranking(industrySort, dateTime)
        exe.rankExtract()
        allResult = [i['result'] for i in exe.result if i['industry'] == '水泥工業'][0]
        rankingResult = [i['result'] for i in exe.rankingResult if i['industry'] == '水泥工業'][0]
        
        assert len(rankingResult) == 3
        assert rankingResult[0]['diff'] > rankingResult[1]['diff'] and rankingResult[1]['diff'] > rankingResult[2]['diff']
        assert rankingResult == [{'ticker': '1103', 'diff': '0.28%'}, {'ticker': '1102', 'diff': '0.23%'}, {'ticker': '1101', 'diff': '-0.13%'}]
        
def test_monthBegin():
    text1101 = '{"stat":"OK","date":"20220701","title":"111年07月 1101 台泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/07/01","21,627,885","854,349,929","39.70","39.75","39.25","39.50","-0.05","7,158"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    text1102 = '{"stat":"OK","date":"20220701","title":"111年07月 1102 亞泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/07/01","6,623,433","289,927,304","4,395","4,415","4,350","4,380","+10","2,462"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    text1103 = '{"stat":"OK","date":"20220701","title":"111年07月 1103 嘉泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/07/01","519,734","9,295,434","17.95","18.10","17.75","18.10","X0.00","332"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    text1104 = '{"stat":"OK","date":"20220701","title":"111年07月 1104 環泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/07/01","789,493","17,283,194","--","--","--","--","X0.00","412"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    text1108 = '{"stat":"OK","date":"20220701","title":"111年07月 1108 幸福             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/07/01","181,093","1,933,283","10.75","10.80","10.60","10.70","-0.10","95"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    last_text1101 = '{"stat":"OK","date":"20220630","title":"111年06月 1101 台泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/30","15,763,786","623,264,030","39.70","39.80","39.40","39.55","-0.05","6,192"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    last_text1102 = '{"stat":"OK","date":"20220630","title":"111年06月 1102 亞泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/30","3,501,258","153,185,252","4,350","4,395","4,350","4,370","+5","2,159"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    last_text1103 = '{"stat":"OK","date":"20220630","title":"111年06月 1103 嘉泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/30","152,262","2,747,807","17.95","18.25","17.95","18.05","-0.25","152"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    last_text1104 = '{"stat":"OK","date":"20220630","title":"111年06月 1104 環泥             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/30","274,838","6,050,601","21.95","22.10","21.90","22.00","-0.05","221"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    last_text1108 = '{"stat":"OK","date":"20220630","title":"111年06月 1108 幸福             各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["111/06/30","47,002","507,420","10.80","10.85","10.75","10.80","-0.10","30"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}'
    with requests_mock.mock() as m:
        m.get("https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220701&stockNo=1101",
            text = text1101,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220701&stockNo=1102",
            text = text1102,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220701&stockNo=1103",
            text = text1103,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220701&stockNo=1104",
            text = text1104,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220701&stockNo=1108",
            text = text1108,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220611&stockNo=1101",
            text = last_text1101,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220611&stockNo=1102",
            text = last_text1102,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220611&stockNo=1103",
            text = last_text1103,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220611&stockNo=1104",
            text = last_text1104,
        )
        m.get(
            "https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20220611&stockNo=1108",
            text = last_text1108,
        )
        industrySort = {'水泥工業': [{'ticker': '1101', 'listed_at': '1962/02/09'}, {'ticker': '1102', 'listed_at': '1962/06/08'}, {'ticker': '1103', 'listed_at': '1969/11/14'}, {'ticker': '1104', 'listed_at': '1971/02/01'}, {'ticker': '1108', 'listed_at': '1990/06/06'}]}
        dateTime = datetime.datetime(2022, 7, 1)
        exe = Ranking(industrySort, dateTime)
        exe.rankExtract()
        allResult = [i['result'] for i in exe.result if i['industry'] == '水泥工業'][0]
        rankingResult = [i['result'] for i in exe.rankingResult if i['industry'] == '水泥工業'][0]
        
        assert len(rankingResult) == 3
        assert rankingResult[0]['diff'] > rankingResult[1]['diff'] and rankingResult[1]['diff'] > rankingResult[2]['diff']
        assert rankingResult == [{'ticker': '1103', 'diff': '0.28%'}, {'ticker': '1102', 'diff': '0.23%'}, {'ticker': '1101', 'diff': '-0.13%'}]
        