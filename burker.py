#from bs4 import BeautifulSoup
# import requests
#import json
#import re
from base import BaseSoup


class Burker(BaseSoup):

    NAME = 'burker'

    def get_name(self):
        return self.soup.find_all('h1', class_='product__title heading-size-9')[0].get_text().replace('\n', '').replace('  ', '')

    def get_brand_id(self):
        return 'burker'

    def get_store_id(self):
        return 'burker'

    # def get_product_id(self):
    #     return self.soup.find_all('div', id="stamped-main-widget")[0].get('data-product-id')

    def get_breadcrumbs(self):
        return []

    def get_price(self):
        price_dict = {}
        fmp_price = self.soup.find_all('span', class_='product__price--sale')[0].get_text().replace('\n', '').replace('  ', '')
        price_dict['fmp'] = fmp_price
        regular_price = self.soup.find_all('span', class_='compare-at em')[0].get_text().replace('\n', '').replace('  ', '')
        if not regular_price:
            regular_price = fmp_price
        price_dict['regular'] = regular_price
        price_dict['currency'] = 'EURO'
        return price_dict

    def get_descr(self):
        return self.soup.find_all('div', class_='accordion-content__holder')[0].get_text().replace('\n', '').replace('  ', '')



