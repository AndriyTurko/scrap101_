#from bs4 import BeautifulSoup
# import requests
import json
import re
from base import BaseSoup


class Degrees(BaseSoup):

    NAME = 'degrees'

    def get_file_name(self):
        file_name = self.page_link.replace('https://www.32degrees.com/products/', '').replace('/', '').split('?')[0]
        return file_name

    def get_json(self):
        text_json = self.soup.find_all('script', id='web-pixels-manager-setup')[0].get_text()
        regex_temp = re.compile(r"(?<=initData\: )(.*})?,},function")
        regex_json = regex_temp.findall(text_json)
        text_json = regex_json[0].replace('\\', '').replace('"{', '{').replace('}"', '}')
        json_end = json.loads(text_json)
        return json_end

    def get_name(self):
        name = self.soup.find_all('h1', class_='!normal-case heading-4 mb-4')[0].get_text()
        return name

    def get_price(self):
        price_dict = {}
        price_l = self.soup.find_all('span', class_='font-bold sale-product:text-accentColor-1')[0]
        fmp_price = price_l.find_all('span', class_='body-2 text-gray-800')[0].get_text().replace('$', '')
        price_dict['fmp'] = fmp_price
        regular_price = price_l.get('data-default-price').replace('$', '')
        if not regular_price:
            regular_price = fmp_price
        price_dict['regular'] = regular_price
        price_dict['currency'] = 'USD'
        return price_dict

    def get_variants(self):
        variants_list = []
        price_dict = self.get_price()
        variants_list.append({
            'cart': 'cart_dict',
            'id': 'x',
            'price': price_dict,
            'selection': 'selection_dict',
            'stock': 'stock_dict',
        })
        return variants_list

    def get_photos(self):
        photos_list = []
        photos_l = self.soup.find_all('div', data_target='product-gallery')
        photos_list.append({'url': 'a'})
        return photos_list

    def get_attributes(self):
        attributes_list = []
        attributes_dict = {}
        values_color_list = []
        color_attr_dict = {}
        color_l = self.soup.find_all('div', class_='atc-sticky:block flex gap-12 lg:gap-16 flex-wrap')[0]
        color_attr_dict['domainType'] = 'color'
        color_attr_dict['id'] = 'color'
        color_attr_dict['label'] = 'Color'
        color_attr_dict['valueType'] = 'Swatch'
        colors = color_l.find_all('input')
        vcl = []
        for c in colors:
            color_name = c.get('value')
            color_id = c.get('id')
            vcl.append({'id': color_id, 'name': color_name, 'swatch': 'swatch'})
        color_attr_dict['values'] = vcl
        values_color_list.append(color_attr_dict)
        attributes_dict['color_values'] = values_color_list

        values_size_list = []
        size_attr_dict = {}
        size_l = self.soup.find_all('div', class_='atc-sticky:block grid sm:grid-cols-6 grid-cols-3 sm:gap-10 gap-16')[0]
        size_attr_dict['domainType'] = 'size'
        size_attr_dict['id'] = 'size'
        size_attr_dict['label'] = 'Size'
        size_attr_dict['valueType'] = 'String'
        sizes = size_l.find_all('input')
        vsl = []
        for s in sizes:
            size_name = s.get('value')
            size_id = s.get('id')
            vsl.append({'id': size_id, 'name': size_name})
        size_attr_dict['values'] = vsl
        values_size_list.append(size_attr_dict)
        attributes_dict['size_values'] = values_size_list
        attributes_list.append(attributes_dict)
        return attributes_list

    def get_brand_id(self):
        return '32degrees'

    def get_store_id(self):
        return '32degrees'

    def get_product_id(self):
        return self.soup.find_all('div', id="stamped-main-widget")[0].get('data-product-id')

    def get_full(self):
        product_id = self.soup.find_all('div', id="stamped-main-widget")[0].get('data-product-id')
        store_id = '32degrees'
        variants = self.get_variants()
        attributes = self.get_attributes()
        #assets = self.get_assets()
        brand_id = '32degrees'
        #breadcrumbs = self.get_breadcrumbs()
        #description = self.get_descr()
        hash = self.get_hash(store_id, product_id, brand_id)
        full_dict = {
            'extractedUrl': self.page_link,
            'hash': hash,
            'product_id': product_id,
            'store_id': store_id,
            'variants': variants,
            #'assets': assets,
            'attributes': attributes,
            'brand': brand_id,
            #'category': breadcrumbs,
            #'description': description,
            'variantSelectors': 'variant_selectors_list',
        }
        return {'product': full_dict}


# <script
#     type='application/json'
#     data-section-data
#   >
