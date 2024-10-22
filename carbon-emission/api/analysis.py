import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

import json
import matplotlib.pyplot as plt
from collections import defaultdict


# 設定全域字體和負號顯示
def load_config():
    plt.rc('font', family='Microsoft JhengHei')
    plt.rcParams['axes.unicode_minus'] = False
    
    # 從 JSON 文件讀取數據
    with open('data.json', 'r', encoding='utf-8') as f:
        records_by_date = json.load(f)
        
    return records_by_date
        

def amount_by_dates(records_by_date):

    # 初始化一個字典來存儲日期和類別的重量
    date_category_weight = defaultdict(lambda: defaultdict(float))

    # 解析數據並進行加總
    for date, records in records_by_date.items():
        for entry in records:
            category = entry[1]
            weight = float(entry[2].split()[0])  # 提取重量
            date_category_weight[date][category] += weight

    # 將數據轉換為 DataFrame 格式
    df = pd.DataFrame(date_category_weight).T.fillna(0)

    # 繪製堆疊柱狀圖
    df.plot(kind='bar', stacked=True, figsize=(12, 8))

    plt.title('各日期類別總重量分析', fontsize=16)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('重量 (kg)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='類別', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def percent_by_items(records_by_date):
    
    # 初始化一個字典來存儲食物類別和總重量
    category_weight = defaultdict(float)

    # 解析數據並進行加總
    for date, records in records_by_date.items():
        for entry in records:
            category = entry[1]
            weight = float(entry[2].split()[0])  # 提取重量
            category_weight[category] += weight

    # 準備繪製圓餅圖的數據
    labels = list(category_weight.keys())
    sizes = list(category_weight.values())

    # 計算總重量，用於計算百分比
    total_weight = sum(sizes)

    # 自定義 autopct 來隱藏小於 1% 的百分比
    def autopct_format(pct):
        return ('%1.1f%%' % pct) if pct >= 1 else ''

    # 只顯示大於 1% 的標籤
    labels = [label if (weight / total_weight) * 100 >= 1 else '' for label, weight in zip(labels, sizes)]

    # 定義顏色地圖，為每個部分分配不同的顏色
    cmap = plt.cm.get_cmap('tab20')  # 使用 'tab20' 顏色圖，最多支持 20 種顏色
    colors = cmap(range(len(labels)))

    # 繪製圓餅圖，將標籤移到外面，並調整距離
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct=autopct_format, startangle=140, 
            labeldistance=1.1, pctdistance=0.85)

    plt.title('各食物類別總重量占比', fontsize=16)
    plt.axis('equal')  # 確保圓餅圖為圓形

    # 調整整個圖形的佈局，避免重疊
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    plt.show()

if __name__ == "__main__":
    percent_by_items()
