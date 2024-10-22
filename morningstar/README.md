# Morningstar

### Requirements

```python
pip install -r requirements.txt
```

### Functions

- `web-scrapper.py`
  - `search_code`: search stock symbol from [morningstar](https://www.morningstar.com/)
  - `beautify_table`: better display for table
  - `get_module`: get the stock module
  - `get_info`: grab the stock info from the module
  - `get_valuation`: get the main features according to the valuation of the stock
  - `write_to_csv`: write the stock info to csv file

- `translate.py`
  - transform the column name to the chinese version


### Output Information

| 英文欄位 | 中文對照 |
|---|---|
|Sector | 產業 |
|Industry | 行業 |
|Investment Style | 投資風格 |
|Price/Book | 市價/帳面價值比 |
|Price/Cash Flow | 市價/現金流量比 |
|Price/Sales | 市價/銷售比 |
|Price/Earnings | 市價/盈利比 |
|Revenue % | 營收增長率 |
|Operating Income % | 營業利潤率 |
|Net Income % | 淨收益率 |
|Diluted EPS % | 稀釋每股盈利率 |
|Quick Ratio* | 速動比率 |
|Current Ratio* | 流動比率 |
|Interest Coverage | 利息保障倍數 |
|Debt/Equity* | 負債/股東權益比率 |
|Return on Assets % | 資產報酬率 |
|Return on Equity % | 股東權益報酬率 |
|Invested Capital % | 投資資本回報率 |
|Net Margin % | 淨利率 |