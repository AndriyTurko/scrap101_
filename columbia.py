#from bs4 import BeautifulSoup
#import requests
import json
import re
from base import BaseSoup


class Columbia(BaseSoup):

    NAME = "columbia"

    def __init__(self, page_link, from_file=True):
        super().__init__(page_link, from_file=from_file)
        self.color_ids = []
        self.json_variation = self.get_json_variation()

    def get_file_name(self):
        return self.page_link.replace('https://www.columbia.com/p/', '').replace('/', '').split('?')[0]

    def get_json_variants(self):
        div = self.soup.find_all('script')
        pattern = 'var variantData = '
        for x in div:
            result = re.search(pattern, x.get_text())
            if result:
                print("Search successful.")
                script = str(x).split(';')
                for y in script:
                    if pattern in y:
                        script_dict = y.replace('var variantData = ', '').replace('  ', '').replace('\n', '')
                        dict_gs = json.loads(script_dict)
                        return dict_gs

    def get_json_variation(self):
        product_id = self.soup.find_all('span', class_='product-id')[0].get_text()
        json_link = ('https://www.columbia.com/on/demandware.store/Sites-Columbia_US-Site/en_US/Product-Variation?pid='
                     + product_id)
        return json.loads(self.get_content(json_link, 'json'))

    def get_variants(self):
        variants_list = []
        cart_dict = {}
        gjv = self.get_json_variants()
        price_dict = self.get_price()
        for x in gjv:
            cart_dict['pid'] = x
            color_id = gjv[x]['color']
            size = gjv[x]['size']
            selection_dict = {'color': color_id, 'size': size}
            availability = gjv[x]['inventory']
            if availability >= 1:
                stock_dict = {
                    'status': 'in_stock',
                    'quantity': availability,
                }
                self.color_ids.append(color_id)
            else:
                continue

            variants_list.append({
                'cart': cart_dict,
                'id': x,
                'price': price_dict,
                'selection': selection_dict,
                'stock': stock_dict,
            })
        return variants_list

    def get_attributes(self):
        attributes_list = []
        color_attr_dict = {}
        attr_l_color = self.soup.find_all('div', class_='attribute js-color-attribute')[0]
        color_l = attr_l_color.find_all('span', class_='swatch__core js-attribute-value color-value')
        selected_color = attr_l_color.find_all('span', class_='swatch__core js-attribute-value color-value selected')
        color_attr_dict['domainType'] = 'color'
        color_attr_dict['id'] = 'color'
        color_attr_dict['label'] = 'Color'
        color_attr_dict['valueType'] = 'swatch'
        qwerty = []
        vcl = []
        for sc in selected_color:
            qwerty.append(sc)
        for c in color_l:
            qwerty.append(c)
        for q in qwerty:
            color_id = q.get('data-attr-value')
            color_name = q.get('title')
            swatch = q.get('style').split('(')[1].replace(')', '').split(',')[0]
            vcl.append({'id': color_id, 'name': color_name, 'swatch': swatch})
        color_attr_dict['values'] = vcl
        attributes_list.append(color_attr_dict)

        size_attr_dict = {}
        attr_l_size = self.soup.find_all('div', class_='attribute js-size-attribute')[0]
        size_l = attr_l_size.find_all('a')
        size_attr_dict['domainType'] = 'size'
        size_attr_dict['label'] = 'Size'
        size_attr_dict['id'] = 'size'
        size_attr_dict['valueType'] = 'string'
        vsl = []
        for s in size_l:
            size_name = s.get('data-attr-hover')
            vsl.append({'id': size_name, 'name': size_name})
        size_attr_dict['values'] = vsl
        attributes_list.append(size_attr_dict)
        return attributes_list

    def get_name(self):
        name = self.soup.find_all("h1", class_="product-name mb-0")[0].get_text()
        return name

    def get_price_value(self, price_l, price_name):
        fmp_price = None
        for x in price_l.find_all('span', class_='value'):
            p_name = x.find_all('span')[0].get_text()
            if price_name in p_name:
                fmp_price = x.get('content')
                break
        return fmp_price

    def get_price(self):
        price_dict = {}
        price_l = self.soup.find_all('div', class_='price')[0]
        fmp_price = self.get_price_value(price_l, 'Regular price:')
        price_dict['fmp'] = fmp_price
        regular_price = self.get_price_value(price_l, 'Sale price:')
        if not regular_price:
            regular_price = fmp_price
        price_dict['regular'] = regular_price
        currency = price_l.find_all('meta', itemprop="priceCurrency")[0].get('content')
        price_dict['currency'] = currency
        message_l = self.soup.find_all('div', class_='js-rewards-container')
        if message_l:
            message = message_l[0].get_text().replace('\n', '').replace('  ', '')
            price_dict['message'] = message
        return price_dict

    def get_descr(self):
        descr_l = self.soup.find_all("div", id="product-accordion-details")[0].find_all("li", class_="pdp-list__item")
        descr = ''
        for x in descr_l:
            descr += x.get_text() + '\n'
        return descr

    def get_breadcrumbs(self):
        bread_list = []
        breads = self.soup.find_all('div', class_='product-breadcrumb')[0].find_all("a")
        for x in breads:
            bread = x.get_text().replace('\n', '').replace('amp;', '').replace('  ', '')
            bread_list.append(bread)
        return bread_list
    
    def get_assets(self):
        assets_list = []
        ids_path = self.json_variation['product']['variationAttributes'][0]['values']
        for x in ids_path:
            assets_dict = {}
            videos_list = []
            images_list = []
            if x['id'] in self.color_ids:
                assets_dict['selector'] = {'color': x['id']}
                for q in x['images']['large']:
                    if 'videoUrl' in q:
                        video = {'url': q['videoUrl']}
                        videos_list.append(video)
                    else:
                        images = {'url': q['url']}
                        images_list.append(images)
                assets_dict['images'] = images_list
                assets_dict['video'] = videos_list
                assets_list.append(assets_dict)
        return assets_list

    def get_brand_id(self):
        return 'columbia'

    def get_store_id(self):
        return 'columbia'

    def get_product_id(self):
        return self.json_variation['queryString'].replace('pid=', '')

    def get_variantSelectors(self):
        return []
