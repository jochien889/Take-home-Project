from module.stockListUpsert import StockList

if __name__=='__main__':
    exe = StockList()
    exe.stockListExtract()
    print('resultList: ', len(exe.resultList))
    print('finalResultList: ', len(exe.finalResultList))