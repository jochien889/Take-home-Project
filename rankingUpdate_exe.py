from module.rankingUpdate import Ranking
import datetime,json, pytz

if __name__=='__main__':
    with open("result/listed.json", 'r', encoding="utf8") as loadFile:
        stockInfo = json.load(loadFile)
        
    dateTime = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
    industrySort = dict()
    for i in stockInfo:
        if i['industry'] in industrySort.keys():
            industrySort[i['industry']].append({ 'ticker': i['ticker'], 'listed_at': i['listed_at']})
        else:
            industrySort[i['industry']] = [{ 'ticker': i['ticker'], 'listed_at': i['listed_at']}]
    filiter = ['水泥工業']
    test = {key:value for key, value in industrySort.items() if key in filiter}

    exe = Ranking(test, dateTime, isSave = True)
    exe.rankExtract()