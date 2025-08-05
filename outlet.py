#from bs4 import BeautifulSoup
# import json
# import re
import os
import requests
from base import BaseSoup


class Outlet(BaseSoup):

    NAME = 'outlet'

    def get_brand_id(self):
        return 'outlet'

    def get_store_id(self):
        return 'outlet'

    def get_breadcrumbs(self):
        bread_list = []
        path = self.soup.find_all('div', class_='product-breadcrumb')[0]
        for x in path.find_all('li'):
            breadcrumb = x.get_text().replace(' ', '').replace('\n', '').replace('\r', '')
            bread_list.append(breadcrumb)
        gender = path.find_all('span', class_='gender')[0].get_text().replace(' ', '').replace('\n', '')
        bread_list.append(gender)
        return bread_list

    def get_descr(self):
        return self.soup.find_all('accordion-component', class_="open")[0].get_text().replace('\n', '').replace('  ', '')

    def get_price(self):
        price_dict = {}
        path = self.soup.find_all('div', class_="price")[0]
        fmp_price = path.find_all('span', class_="value")[0].get('content')
        price_dict['fmp'] = fmp_price
        regular_price = path.find_all('span', class_="sales font-body-large")[0].find('span').get('content')
        if not regular_price:
            regular_price = fmp_price
        price_dict['regular'] = regular_price
        price_dict['currency'] = 'USD'
        message = path.find_all('span', class_="savings")[0].get_text().replace('\n', '').replace('  ', '')
        price_dict['message'] = message
        return price_dict

    def get_content(self, page_url, file_extention='txt'):
        header = {
            'User-Agent': 'Mozilla/5(Macintosh; Intel Mac OS X 10_15_7)',
            'referer': 'https://www.joesnewbalanceoutlet.com/pd/2002r/M2002RV1-45663.html'
        }
        super().get_content(page_url, file_extention='txt', headers=header)

    def get_attributes(self):
        attributes_list = []
        color_attr_dict = {}
        color_attr_dict['domainType'] = 'color'
        color_attr_dict['id'] = 'color'
        color_attr_dict['label'] = 'Color'
        color_attr_dict['valueType'] = 'swatch'
        vcl = []
        color_path = self.soup.find_all('div', class_='color-style attribute-grid-3 null')[0]
        for x in color_path.find_all('button'):
            color_id = x.get('title')
            color_name = x.get('data-variation-value')
            swatch = x.find('span').get('style').replace(')', '').split('(')[-1]
            vcl.append({'id': color_id, 'name': color_name, 'swatch': swatch})
        color_attr_dict['values'] = vcl
        attributes_list.append(color_attr_dict)

        size_attr_dict = {}
        size_path = self.soup.find_all('div', class_='select-attribute-grid attribute-grid-5 null')[0]
        size_attr_dict['domainType'] = 'size'
        size_attr_dict['id'] = 'size'
        size_attr_dict['label'] = 'Size'
        size_attr_dict['valueType'] = 'string'
        vsl = []
        for x in size_path.find_all('button'):
            size_id = x.get('data-variantid')
            size_name = x.get('title')
            vsl.append({'id': size_id, 'name': size_name})
        size_attr_dict['values'] = vsl
        attributes_list.append(size_attr_dict)
        return attributes_list

    def get_assets(self):
        assets_list = []
        assets_dict = {}
        path_photo = self.soup.find('div', class_='carousel-inner carousel-desktop')
        for x in path_photo.find_all('button', class_='p-0 w-100'):
            photo = x.get('data-src')
        path_color = ''

        return assets_list



