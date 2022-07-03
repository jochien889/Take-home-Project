# Take-home-Project

# 開發環境設定
1. 安裝pipenv
2. 建立python 3.9虛擬環境
3. 安裝專案所需套件
4. 輸出requirements.txt

``` shell
pip install pipenv 
pipenv --python 3.9.7
pipenv install pytest requests lxml pandas
pipenv lock --requirements > requirements.txt
```

# 本機環境部屬
1. 取得Repository
2. 建立專案環境
3. 進入專案環境
4. 安裝requirements.txt
5. 獲取virtualenv位置執行crontab
* (範例: 一到五10點執行stockListUpsert_exe.py更新listed.json, 一到五13點30執行rankingUpdate_exe.py更新top3.json)

``` shell
git clone https://github.com/jochien889/Take-home-Project.git
pipenv 
pipenv shell
pip install -r requirements.txt
0  10  *  *  1-5  Take-home-Project-vNGbLYxG/bin/python Take-home-Project/stockListUpsert_exe.py
30  13  *  *  1-5  Take-home-Project-vNGbLYxG/bin/python Take-home-Project/rankingUpsert_exe.py
```

# 線上環境部屬
1. 使用github + AWS codeBuild 部屬到AWS Lambda
2. 上市的股票資訊存入AWS RDS，可幫助資料庫正規化處理
3. top3名單每日更新存入AWS RDS，使用AWS Lambda將每日更新名單存入S3作為log
4. top3拉取時間太久，可多開VPC IP配合多個Lambda function 同步處理資料
