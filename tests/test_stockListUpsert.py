import requests_mock
from module.stockListUpsert import stockListExtract

def test_text():
    # first_test  ="<head></html>"
    mockText ="""
                <link rel="stylesheet" href="http://isin.twse.com.tw/isin/style1.css" type="text/css">\n      <body><table  align=center><h2><strong><font class=\'h1\'>本國上市證券國際證券辨識號碼一覽表</font></strong></h2><h2><strong><font class=\'h1\'><center>最近更新日期:2022/06/30  </center> </font></strong></h2><h2><font color=\'red\'><center>掛牌日以正式公告為準</center></font></h2></table><TABLE class=\'h4\' align=center cellSpacing=3 cellPadding=2 width=750 border=0><tr align=center><td bgcolor=#D5FFD5>有價證券代號及名稱 </td><td bgcolor=#D5FFD5>國際證券辨識號碼(ISIN Code)</td><td bgcolor=#D5FFD5>上市日</td><td bgcolor=#D5FFD5>市場別</td><td bgcolor=#D5FFD5>產業別</td><td bgcolor=#D5FFD5>CFICode</td><td bgcolor=#D5FFD5>備註</td></tr>
                <tr><td bgcolor=#FAFAD2 colspan=7 ><B> 股票 <B> </td></tr>
                <tr><td bgcolor=#FAFAD2>1101\u3000台泥</td><td bgcolor=#FAFAD2>TW0001101004</td><td bgcolor=#FAFAD2>1962/02/09</td><td bgcolor=#FAFAD2>上市</td><td bgcolor=#FAFAD2>水泥工業</td><td bgcolor=#FAFAD2>ESVUFR</td><td bgcolor=#FAFAD2></td></tr>
                <tr><td bgcolor=#FAFAD2>1102\u3000亞泥</td><td bgcolor=#FAFAD2>TW0001102002</td><td bgcolor=#FAFAD2>1962/06/08</td><td bgcolor=#FAFAD2>上市</td><td bgcolor=#FAFAD2>水泥工業</td><td bgcolor=#FAFAD2>ESVUFR</td><td bgcolor=#FAFAD2></td></tr>
                <tr><td bgcolor=#FAFAD2>1103\u3000嘉泥</td><td bgcolor=#FAFAD2>TW0001103000</td><td bgcolor=#FAFAD2>1969/11/14</td><td bgcolor=#FAFAD2>上市</td><td bgcolor=#FAFAD2>水泥工業</td><td bgcolor=#FAFAD2>ESVUFR</td><td bgcolor=#FAFAD2></td></tr>
                <tr><td bgcolor=#FAFAD2>1104\u3000環泥</td><td bgcolor=#FAFAD2>TW0001104008</td><td bgcolor=#FAFAD2>1971/02/01</td><td bgcolor=#FAFAD2>上市</td><td bgcolor=#FAFAD2>水泥工業</td><td bgcolor=#FAFAD2>ESVUFR</td><td bgcolor=#FAFAD2></td></tr>
                <tr><td bgcolor=#FAFAD2>1108\u3000幸福</td><td bgcolor=#FAFAD2>TW0001108009</td><td bgcolor=#FAFAD2>1990/06/06</td><td bgcolor=#FAFAD2>上市</td><td bgcolor=#FAFAD2>水泥工業</td><td bgcolor=#FAFAD2>ESVUFR</td><td bgcolor=#FAFAD2></td></tr>
                <tr><td bgcolor=#FAFAD2>1109\u3000信大</td><td bgcolor=#FAFAD2>TW0001109007</td><td bgcolor=#FAFAD2>1991/12/05</td><td bgcolor=#FAFAD2>上市</td><td bgcolor=#FAFAD2>水泥工業</td><td bgcolor=#FAFAD2>ESVUFR</td><td bgcolor=#FAFAD2></td></tr>
                <tr><td bgcolor=#FAFAD2>1110\u3000東泥</td><td bgcolor=#FAFAD2>TW0001110005</td><td bgcolor=#FAFAD2>1994/10/22</td><td bgcolor=#FAFAD2>上市</td><td bgcolor=#FAFAD2>水泥工業</td><td bgcolor=#FAFAD2>ESVUFR</td><td bgcolor=#FAFAD2></td></tr>
                """
    with requests_mock.mock() as m:
        m.get(
            "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",
            text = mockText,
        )
        result = stockListExtract()
        print(result)
        assert len(result) == 7
        
def test_invalid_text():
    mockText  ="<head></html>"
    with requests_mock.mock() as m:
        m.get(
            "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",
            text = mockText,
        )
        result = stockListExtract()
        print(result)
        assert len(result) == 0

