import requests_mock
from module.stockListUpsert import stockListExtract

def test_stockListExtract():
    """"""

    first_test = mockSample1 ="<head></html>"
    with requests_mock.mock() as m:
        m.get(
            "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",
            text = first_test,
        )
        test1_result = stockListExtract()
        # assert len(test1_result) == 0
        print(test1_result)
        

