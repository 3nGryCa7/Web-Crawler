# import libraries for data processing
import pandas as pd
# import libraries for web scraping
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import libraries for visualization
from IPython.display import display
# import libraries for file processing
import os

# from selenium.webdriver.chrome.options import Options
# set up browser options (不支援 Edge)
# browser_options = Options()
# browser_options.add_argument("--headless")  # 啟用 Headless 模式


def search_code(code: str) -> pd.DataFrame:
    """Function: Search the stock code from Morningstar"""
    
    # set search url
    url = f'https://www.morningstar.com/search?query={code}'

    # get the response in the form of html
    response = requests.get(url)

    # if response is ok then go ahead and parse the response
    if response.status_code == 200:
        companys = _query_search(response)
    return companys


def _query_search(response: requests.models.Response) -> pd.DataFrame:
    """Function: Parse the response from html into a beautifulsoup object"""

    # parse the response from html into a beautifulsoup object
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = soup.find_all('a', class_='mdc-link mdc-security-module__name mds-link mds-link--no-underline mdc-link--no-underline')
    modules = soup.find_all('span', class_="mdc-security-module__exchange")

    # Create lists to store the data
    title_list = [title.get_text() for title in titles]
    module_list = [module.get_text() for module in modules]

    return pd.DataFrame({'Company': title_list, 'Module': module_list})


def beautify_table(companys: pd.DataFrame) -> None:
    """Function: Beautify the table"""

    # 創建 Styler 物件
    styler = companys.style

    # 設定欄位的文字對齊為置中
    styles = [
        {'selector': '.col_heading', 'props': [('text-align', 'center')]},
        {'selector': '.data', 'props': [('text-align', 'left')]},
    ]
    styler.set_table_styles(styles)

    # 顯示 DataFrame
    display(styler)


def get_module(companys: pd.DataFrame) -> str:
    """Function: Get the module"""

    # get the stock module
    try: 
        stock = int(input("Enter the company index: "))
        # get the stock code
        module = companys.iloc[stock, 1]
    except:
        raise ValueError("Not a number")

    return module.lower()


# get Sector、Industry、Investemnt Style、Beta

# Overview、Key Ratios、Trading Information 都是同一個class同一頁面
# 用指定的class找到目標element，再根據element的index找到對應的value

def get_info(code: str, driver: webdriver.edge.webdriver.WebDriver) -> pd.DataFrame:

    # set the url
    url = f'https://www.morningstar.com/stocks/xtai/{code}/quote'

    # get into the url
    driver.get(url)

    # [:2] is Sector and Industry
    industries = driver.find_elements("css selector", ".mdc-data-point.mdc-data-point--string")
    # style only have one element
    target_span = driver.find_elements("css selector", ".mdc-data-point.mdc-data-point--style-box")
    # get the style
    style = ''.join(span.text for span in target_span if span.text != '')

    return pd.DataFrame({'Sector': [industries[0].text], 'Industry': [industries[1].text], 'Investment Style': [style]})


def get_valuation(code: str, driver: webdriver.edge.webdriver.WebDriver) -> pd.DataFrame:
    """Function: Get the stock quote from Morningstar"""

    # set the url
    url = f'https://www.morningstar.com/stocks/xtai/{code}/valuation'

    # get into the url
    driver.get(url)

    # get key statistics
    # Explicitly wait for key statistics to be present
    wait = WebDriverWait(driver, 10)
    key_classes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sal-panel-header")))
    key_names = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dp-name")))
    key_values = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dp-value")))

    key_class = [key_class.text for key_class in key_classes]
    key_names = [key_name.text for key_name in key_names]
    key_values = [key_value.text for key_value in key_values]

    # for i in range(len(key_class)):
    #     print(key_class[i])
    #     beautify_table(pd.DataFrame({'Key': key_names[i*4:(i+1)*4], 'Value': key_values[i*4:(i+1)*4]}))

    return pd.DataFrame([key_values], columns=key_names)


def write_to_csv(data: pd.DataFrame, filename: str) -> None:
    """Function: Write the data into a csv file"""

    # get the current working directory
    current_path = os.getcwd()

    # set the file path
    file_path = os.path.join(current_path, filename)

    # check if the file exists and is empty
    if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
        # create a new file and write both column names and data
        data.to_csv(file_path, index=False, encoding='utf-8-sig')
    else:
        # append data to an existing file without column names
        data.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8-sig')


import os

def write_to_csv(data: pd.DataFrame, filename: str) -> None:
    """Function: Write the data into a csv file"""

    # get the current working directory
    current_path = os.getcwd()

    # set the file path
    file_path = os.path.join(current_path, filename)

    # check if the file exists and is empty
    if os.path.exists(file_path) and os.path.isfile(file_path) and os.stat(file_path).st_size > 0:
        _do_write_to_csv_16(file_path, data)
    else:
        # create a new file and write both column names and data
        data.to_csv(file_path, index=False, encoding='utf-8-sig')

# write the data to the csv file
def _do_write_to_csv_16(file_path, data):
    # read existing data from the file
    existing_data = pd.read_csv(file_path)
    # to_csv() will convert the stock code to int, so we need to convert it back to str
    existing_data['Stock Code'] = existing_data['Stock Code'].astype(str)

    # find duplicate stock codes in the new data
    duplicates = data[data['Stock Code'].isin(existing_data['Stock Code'].values)]

    if not duplicates.empty:
        # remove existing rows with duplicate stock codes
        existing_data = existing_data[~existing_data['Stock Code'].isin(duplicates['Stock Code'].values)]

    # concatenate existing data with the new data
    updated_data = pd.concat([existing_data, data], ignore_index=True)

    # write the updated data to the file
    updated_data.to_csv(file_path, index=False, encoding='utf-8-sig')


# method: get to start the program

def __main__():
    # set up the browser
    driver = webdriver.Edge()

    # get the stock code
    stock_code = input("Enter the stock code: ")

    ### Mostly is 'xtai' ###

    # if not, then... do following steps

    # do the search
    # companys = search_code(stock_code)
    # beautify_table(companys)

    # get the module

    basic_info = get_info(stock_code, driver)
    # basic_info.rename(index={0: f"{stock_code}"}, inplace=True)

    key_statistics = get_valuation(stock_code, driver)
    
    # merge the two dataframes
    merged = pd.concat([basic_info, key_statistics], axis=1)
    # insert the stock code into the first column
    merged.insert(0, 'Stock Code', stock_code)

    beautify_table(merged)

    # write the data to the csv file
    write_to_csv(merged, 'stocks.csv')

    # close the browser
    driver.quit()


if __name__ == '__main__':
    __main__()