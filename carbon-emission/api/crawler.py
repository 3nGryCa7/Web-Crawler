import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from dotenv import load_dotenv
import time
from collections import defaultdict

def crawl_data():
    # 從 .env 文件加載帳號和密碼
    load_dotenv()

    email = os.getenv("EMAIL")  # 從 .env 讀取帳號
    password = os.getenv("PASSWORD")  # 從 .env 讀取密碼

    # Edge 瀏覽器選項
    options = Options()
    options.use_chromium = True  # 使用 Chromium 內核的 Edge
    options.add_argument("--start-maximized")  # 最大化瀏覽器
    options.add_argument('--ignore-certificate-errors')  # 忽略 SSL 錯誤
    options.add_argument("--headless")  # 無頭模式

    # 初始化 Edge WebDriver
    driver = webdriver.Edge(options=options)

    try:
        # 1. 打開登入頁面並登入
        driver.get("https://mcrp.jwfu.me/login")
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)

        # 2. 轉向爬取頁面並抓取數據
        driver.get("https://mcrp.jwfu.me/records")
        record_rows = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'record-')]")
        records_by_date = defaultdict(list)

        for row in record_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            data = [column.text for column in columns]
            record_date = data[0].split()[0]  # 只提取日期
            records_by_date[record_date].append(data)

        # 將數據寫入 JSON 文件
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(records_by_date, f, ensure_ascii=False, indent=4)

    finally:
        driver.quit()
