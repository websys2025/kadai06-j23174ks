import requests

#自分のアプリケーションID
APP_ID = "4d65ea9c5f60e492deb6e20461adb2094ae5712d"

#e-Stat APIのエンドポイント
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

#リクエストパラメータ設定
params = {
    "appId": APP_ID,
    "statsDataId": "0003107553",   # 労働力調査（基本集計）- 完全失業率（年平均）
    "cdArea": "00000",             # 全国（地域コード）
    "cdCat01": "000110",           # 完全失業率
    "metaGetFlg": "Y",             # メタ情報も取得
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
    "lang": "J"                    # 日本語で取得
}

#APIへリクエストを送信
response = requests.get(API_URL, params=params)

#応答をJSONとして処理
data = response.json()

print("==== 完全失業率（年平均）のデータ取得 ====")
if "GET_STATS_DATA" in data:
    stats_data = data["GET_STATS_DATA"]
    if "STATISTICAL_DATA" in stats_data:
        for item in stats_data["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]:
            print(f"年: {item.get('@time')}, 値: {item.get('$')}")
    else:
        print("統計データが見つかりませんでした。")
else:
    print("APIからの応答に問題があります。")
