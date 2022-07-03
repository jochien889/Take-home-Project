from module.rankingUpsert import Ranking
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

    exe = Ranking(industrySort, dateTime)
    exe.rankExtract()
    finalResult = exe.rankingResult
    for i in finalResult:
        with open("result/{}_top3.json".format(i['industry']), 'w') as File:
            json.dump(i['result'], File, ensure_ascii = False)