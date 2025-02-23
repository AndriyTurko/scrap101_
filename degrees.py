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

    def get_json_variants(self):
        text_json = self.soup.find_all('script', id='web-pixels-manager-setup')[0].get_text()
        regex_temp = re.compile(r"(?<=initData\: )(.*})?,},function")
        regex_json = regex_temp.findall(text_json)
        text_json = regex_json[0].replace('\\', '').replace('"{', '{').replace('}"', '}')
        json_end = json.loads(text_json)
        return json_end

    def get_json_assets(self):
        text_json = self.soup.find_all('main', id='MainContent')[0].find_all('script')[0].get_text()
        json_end = json.loads(text_json)
        return json_end['images']['colorGroupImages']

    def get_name(self):
        return self.soup.find_all('h1', class_='!normal-case heading-4 mb-4')[0].get_text()

    def get_descr(self):

        title = (self.soup.find_all('summary', class_='relative !list-none pb-18 pt-10 lg:pb-24 lg:pt-16')[0].get_text()
                 .replace('\n', ''))
        path_descr = (self.soup.find_all('ul', class_='metafield-single_line_text_field-array')[0]
                      .find_all('li', class_="metafield-single_line_text_field"))
        options = ''
        for x in path_descr:
            options += ', ' + x.get_text()
        return title + options

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
        gj = self.get_json_variants()
        price_dict = self.get_price()
        variants_list = []
        path_quantity = json.loads(self.soup.find_all('form', id='add-to-cart-form')[0].get('data-variants'))
        quantity_dict = {q['id']: q['inventory_quantity'] for q in path_quantity}
        #if q['inventory_quantity'] >= 1:
        for x in gj['productVariants']:
            variant_id = int(x['id'])
            if variant_id in quantity_dict and quantity_dict[variant_id] > 0:
                path_selection = x['title'].split('/')
                color = path_selection[0].strip(' ')
                size = path_selection[1].strip(' ')
                selection_dict = {'color': color, 'size': size}
                cart_dict = {'id': x['id'], 'sku': x['sku']}
                stock_dict = {'status': 'in_stock', 'quantity': quantity_dict[variant_id]}
                variants_list.append({
                    'cart': cart_dict,
                    'price': price_dict,
                    'selection': selection_dict,
                    'stock': stock_dict,
                })
        return variants_list

    def get_assets(self):
        assets_list = []
        gja = self.get_json_assets()
        for x in gja:
            assets_dict = {}
            assets_dict['selector'] = {'color': x}
            images_list = []
            videos_list = []
            for i in gja[x]:
                images = i['large'].replace('//', '')
                images_list.append({'url': images})
                assets_dict['images'] = images_list
                assets_dict['videos'] = videos_list
            assets_list.append(assets_dict)
        return assets_list

    def get_attributes(self):
        attributes_list = []
        color_attr_dict = {}
        color_l = self.soup.find_all('div', class_='atc-sticky:block flex gap-12 lg:gap-16 flex-wrap')[0]
        color_attr_dict['domainType'] = 'color'
        color_attr_dict['id'] = 'color'
        color_attr_dict['label'] = 'Color'
        color_attr_dict['valueType'] = 'rgb'
        colors = color_l.find_all('input')
        vcl = []
        path_rgbs = self.soup.find_all('div', class_='atc-sticky:block flex gap-12 lg:gap-16 flex-wrap')[0]
        rgb_l = path_rgbs.find_all('span')
        for c in colors:
            color_name = c.get('value')
            for r in rgb_l:
                path_rgb = r.get('style')
                if path_rgb:
                    rgb = path_rgb.split(':')[1].replace(';', '').replace(' ', '')
                    vcl.append({'id': color_name, 'name': color_name, 'rgb': rgb})
        color_attr_dict['values'] = vcl
        attributes_list.append(color_attr_dict)

        size_attr_dict = {}
        size_l = self.soup.find_all('div', class_='atc-sticky:block grid sm:grid-cols-6 grid-cols-3 sm:gap-10 gap-16')[0]
        size_attr_dict['domainType'] = 'size'
        size_attr_dict['id'] = 'size'
        size_attr_dict['label'] = 'Size'
        size_attr_dict['valueType'] = 'string'
        sizes = size_l.find_all('input')
        vsl = []
        for s in sizes:
            size_name = s.get('value')
            size_id = s.get('id')
            vsl.append({'id': size_id, 'name': size_name})
        size_attr_dict['values'] = vsl
        attributes_list.append(size_attr_dict)
        return attributes_list

    def get_brand_id(self):
        return '32degrees'

    def get_store_id(self):
        return '32degrees'

    def get_product_id(self):
        return self.soup.find_all('div', id="stamped-main-widget")[0].get('data-product-id')

    def get_breadcrumbs(self):
        return []



