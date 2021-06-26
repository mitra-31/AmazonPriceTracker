from bs4 import BeautifulSoup
import requests



header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

##############################################################################################################
#                                                                                                            #
#                               Scraping Method .                                                            #
#                                                                                                            #
# To get product inside the url by using "id" : "productTitle" .                                             #           
# To get price of product inside the url by using "id":"priceblock_ourprice" or "id":"priceblock_dealprice" .#
#                                                                                                            #
##############################################################################################################
def scrape(url):
    page = requests.get(url,headers=header)
    soup = BeautifulSoup(page.content,'html.parser')
    
    product = soup.find(id="productTitle").get_text().strip()
    
    try:
        price = soup.find(id = 'priceblock_ourprice').get_text()
    except Exception as e:
        price = soup.find(id = 'priceblock_dealprice').get_text()
    except Exception as e:
        price = soup.find(id = 'priceBlockBuyingPriceString').get_text()

    #print(price)
    return product,price