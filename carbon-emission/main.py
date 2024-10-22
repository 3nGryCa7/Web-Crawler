from api.crawler import crawl_data
from api.analysis import amount_by_dates, percent_by_items, load_config

def main():
    # crawl_data()  # run it if first time
    data = load_config()
    amount_by_dates(data)
    percent_by_items(data)

if __name__ == '__main__':
    
    main()
