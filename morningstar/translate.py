import pandas as pd

pd.set_option('display.max_columns', None)

# Read in the data
stocks = pd.read_csv('stocks.csv', index_col=0)


# 定義新的欄位名稱列表
new_columns = ['產業', '行業', '投資風格', 'P/B', 'P/CF', 'P/S', 'P/E', '營收增長率',
               '營業利潤率', '淨利率', '稀釋每股盈利率', '速動比率', '流動比率', '利息保障倍數', 'D/E',
               '資產報酬率', '股東權益報酬率', '投資資本回報率', '淨利率']

# 使用 rename() 函數更改欄位名稱
stocks = stocks.rename(columns=dict(zip(stocks.columns, new_columns)))

print(stocks)