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

    def get_product_id(self):
        return 'burker'

    def get_breadcrumbs(self):
        return []

    def get_price(self):
        price_dict = {}
        fmp_price = self.soup.find_all('span', class_='product__price--sale')[0].get_text().replace('\n', '').replace('  ', '').replace('\u20ac', '')
        price_dict['fmp'] = fmp_price
        regular_price = self.soup.find_all('span', class_='compare-at em')[0].get_text().replace('\n', '').replace('  ', '').replace('\u20ac', '')
        if not regular_price:
            regular_price = fmp_price
        price_dict['regular'] = regular_price
        price_dict['currency'] = 'EURO'
        return price_dict

    def get_variants(self):
        price_dict = self.get_price()
        variants_list = []
        quantity = self.soup.find_all('script', id="back-in-stock-helper")[0].get_text().split("['inventory_quantity'] = ")[-1].replace(';', '').replace('\n', '')
        color = self.soup.find_all('div', class_='product__media')[0].get('aria-label')
        if int(quantity) <= 0:
            stock_dict = {'status': 'not_in_stock', 'quantity': quantity}
        else:
            stock_dict = {'status': 'in_stock', 'quantity': quantity}
        variants_list.append({
            'cart': 'cart_dict',
            'price': price_dict,
            'selection': {'color': color},
            'stock': stock_dict,
        })
        return variants_list

    def get_descr(self):
        return self.soup.find_all('div', class_='accordion-content__holder')[0].get_text().replace('\n', '').replace('  ', '')

    def get_assets(self):
        assets_list = []
        path = self.soup.find_all('div', class_='product__media')
        video = self.soup.find_all('div', class_='media__contain')[0].find('video').find('source').get('src')
        for x in path:
            assets_dict = {}
            images_list = []
            videos_list = []
            images = x.find('img').get('srcset')
            images_list.append({'url': images})
            videos_list.append({'url': video})
            color = x.find('img').get('alt')
            assets_dict['selector'] = {'color': color}
            assets_dict['images'] = images_list
            assets_dict['videos'] = videos_list
            assets_list.append(assets_dict)
        return assets_list

    def get_attributes(self):
        attributes_list = []
        attributes_dict = {}
        attributes_dict['domainType'] = 'color'
        attributes_dict['id'] = 'color'
        attributes_dict['label'] = 'Color'
        attributes_dict['valueType'] = 'string'
        return attributes_list



