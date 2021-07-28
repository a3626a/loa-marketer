import time
import json
import random
import requests
from bs4 import BeautifulSoup

# {
#   itemno: price,
#   ...
# }
# page 는 1 페이지부터 시작한다.
def getRecentPricesOfPage(category, page):
    response = requests.get(
        "https://lostark.game.onstove.com/Market/List_v2",
        params = {
            'firstCategory': str(category),
            'secondCategory': '0',
            'tier': '0',
            'grade': '99',
            'itemName': '',
            'pageNo': str(page),
            'isInit': 'false',
            'sortType': '7',
            '_': str(int(time.time()*1000))
        }
    )
    ret = {}
    soup = BeautifulSoup(response.text, 'html.parser')
    for i in soup.find(id="tbodyItemList").find_all('tr') :
        if i.has_attr('class') and 'empty' in i['class'] :
            break
        price_tags = i.find_all(class_="price")
        prices = [tag.em.string for tag in price_tags]
        yesterday_avg, last, lowest = prices
        itemno = i.find(class_="button--deal-buy")['data-itemno']
        ret[itemno] = last
    return ret

def getRecentPricesOfCategory(category) :
    prices = {}
    for i in range(1, 100) :
        prices_in_page = getRecentPricesOfPage(category, i)
        
        if not prices_in_page:
            break
        
        prices.update(prices_in_page)
    return prices


def main():
    categories = ['60000', '50000', '70000', '90000', '100000']
    prices = {}
    for cate in categories :
        prices_in_category = getRecentPricesOfCategory(cate)
        prices.update(prices_in_category)

    print(prices)

if __name__ == '__main__' :
    main()