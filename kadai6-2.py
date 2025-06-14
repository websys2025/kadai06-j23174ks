import requests
import pandas as pd

#アプリケーションID
APP_ID = "4d65ea9c5f60e492deb6e20461adb2094ae5712d"

#e-Stat API エンドポイント
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

#リクエストパラメータ（2022年の食費データ、都道府県別）
params = {
    "appId": APP_ID,
    "statsDataId": "0003412317",     # 家計調査（二人以上の世帯）2022年
    "cdCat01": "010100",             # 食費カテゴリ（消費支出）
    "cdArea": "",                    # 空欄で全国すべての地域を取得
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
    "lang": "J"
}

#APIからデータ取得
response = requests.get(API_URL, params=params)
data = response.json()

#統計データ（値部分）の抽出
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
df = pd.DataFrame(values)

#メタ情報の取得と置換処理（IDは名前）
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']
for class_obj in meta_info:
    column_name = '@' + class_obj['@id']
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']
    df[column_name] = df[column_name].replace(id_to_name_dict)

#列名の整形
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

new_columns = [col_replace_dict.get(col, col) for col in df.columns]
df.columns = new_columns

#結果出力（都道府県ごとの食費データ）
print("==== 家計調査：1世帯あたりの食費（都道府県別・年間） ====")
print(df[['時間軸（年次）', '地域', '消費支出項目', '値', '単位']])
