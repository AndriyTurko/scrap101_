#from bs4 import BeautifulSoup
# import json
# import re
# import os
# import requests
from base import BaseSoup
from itertools import zip_longest


class Gap(BaseSoup):

    NAME = 'gap'

    def get_product_id(self):
        return ''

    def get_brand_id(self):
        return 'gap'

    def get_store_id(self):
        return 'gap'

    def get_breadcrumbs(self):
        return []

    def get_descr(self):
        path = self.soup.find_all('div', data_selector="panel panel-product-info")
        print(path)
        return ''

    def get_variants(self):
        variants_list = []
        color_price_path = self.soup.find_all('div', class_='swatch-group swatch-group--color')[0]
        size_path = self.soup.find_all('div', class_='dimension-list--with-size-sampling')[0]
        for cpp, sp in zip_longest(color_price_path, size_path):
            price_dict = {}
            selection_dict = {}

            size = sp.find_all('span')[0].get_text()
            selection_dict['size'] = size

            if cpp:
                prices = cpp.find_all('div', class_='swatch-price swatch-price__inner')[0].get_text().split('$')[1:]
                fmp_price = prices[0]
                price_dict['fmp'] = fmp_price
                regular_price = prices[1]
                if not regular_price:
                    regular_price = fmp_price
                price_dict['regular'] = regular_price
                price_dict['currency'] = 'USD'

                colors = cpp.find_all('div', class_='swatch-price-group__list sitewide-1bll3gl')[0]
                colors_list = []
                for ec in colors:
                    colors_list.append(ec.get_text())
                for color in colors_list:
                    selection_dict['color'] = color
                    # size = sp.find_all('span')[0].get_text()
                    # for s in size:
                    #     selection_dict['size'] = size
                    variants_list.append({
                        'cart': 'cart_dict',
                        'price': price_dict,
                        'selection': selection_dict,
                        'stock': 'stock_dict',
                    })
        return variants_list

    def get_attributes(self):
        attributes_list = []
        color_attr_dict = {}
        color_attr_dict['domainType'] = 'color'
        color_attr_dict['id'] = 'color'
        color_attr_dict['label'] = 'Color'
        color_attr_dict['valueType'] = 'swatch'
        vcl = []
        color_path = self.soup.find_all('div', class_='swatch-group swatch-group--color')[0]
        for cp in color_path:
            colors = cp.find_all('div', class_='swatch-price-group__list sitewide-1bll3gl')[0]
            for c in colors:
                color = c.get_text()
                vcl.append({'id': color, 'name': color, 'swatch': 'swatch'})
            color_attr_dict['values'] = vcl
        attributes_list.append(color_attr_dict)

        size_attr_dict = {}
        size_attr_dict['domainType'] = 'size'
        size_attr_dict['id'] = 'size'
        size_attr_dict['label'] = 'Size'
        size_attr_dict['valueType'] = 'string'
        vsl = []
        size_path = self.soup.find_all('div', class_='dimension-list--with-size-sampling')[0]
        for sp in size_path:
            size = sp.find_all('span', class_="pdp-dimension__text")[0].get_text()
            vsl.append({'id': size, 'name': size})
            size_attr_dict['values'] = vsl
        attributes_list.append(size_attr_dict)
        return attributes_list

    def get_assets(self):
        assets_list = []
        assets_dict = {}
        photos_list = []
        videos_list = []
        path = self.soup.find_all('div', class_='product_photos-container')[0]
        for x in path.find_all('div', class_='brick__product-image-wrapper'):
            photo = 'https://www.gap.com/' + x.find_all('a')[0].get('href')
            photos_list.append({'url': photo})
        assets_dict['images'] = photos_list
        assets_dict['videos'] = videos_list
        assets_list.append(assets_dict)
        return assets_list
