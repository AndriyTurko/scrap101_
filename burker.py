#from bs4 import BeautifulSoup
# import requests
import json
import re
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
        return self.soup.find_all('product-form', class_="product__block__buttons")[0].find('input', attrs={'type':'hidden', 'name':'product-id'}).get('value')

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
        attributes_json = self.get_attributes_json()
        localisation_dict = {'срібло': 'silver', 'золото': 'gold'}
        variants_list = []
        script_tag = self.soup.find_all('script', id="back-in-stock-helper")[0]#.get_text().split("['inventory_quantity'] = ")[-1].replace(';', '').replace('\n', '')
        product_id = self.soup.find_all('product-form', class_="product__block__buttons")[0].find('input', attrs={'type':'hidden', 'name':'product-id'}).get('value')
        section_id = self.soup.find_all('product-form', class_="product__block__buttons")[0].find('input', attrs={
            'type': 'hidden', 'name': 'section-id'}).get('value')

        for i, x in enumerate(attributes_json):
            if not x['public_title']:
                variant_id = self.soup.find_all('product-form', class_="product__block__buttons")[0].find('input', attrs={'type': 'hidden', 'name': 'id'}).get('value')
                color_name = self.soup.find_all('div', class_='product__media')[0].get('aria-label')
                quantity = self.soup.find_all('script', id="back-in-stock-helper")[
                    0].get_text().split("['inventory_quantity'] = ")[-1].replace(';', '').replace('\n', '').replace(' ', '')
                variants_list.append({
                    'cart': {'variant_id': variant_id, 'product_id': product_id, 'section_id': section_id},
                    'price': price_dict,
                    'selection': {'color': color_name},
                    'stock': {"status": "in_stock", "quantity": int(quantity)},
                })
            else:
                color_name = x['public_title'].lower()
                variant_id = x['id']
                if color_name in localisation_dict:
                    color_name = localisation_dict[color_name]
                if script_tag:
                    script_content = script_tag.string
                    pattern = re.findall(r"inventory_quantity\'\] = (\d+)", script_content)
                    quantity_list = list(map(int, pattern))
                    quantity = quantity_list[i]
                    if quantity >= 1:
                        stock_dict = {"status": "in_stock", "quantity": int(quantity)}
                    else:
                        stock_dict = {"status": "not_in_stock"}
                    variants_list.append({
                        'cart': {'variant_id': variant_id, 'product_id': product_id, 'section_id': section_id},
                        'price': price_dict,
                        'selection': {'color': color_name},
                        'stock': stock_dict
                    })
        return variants_list

    # def get_variants(self):
    #     price_dict = self.get_price()
    #     variants_list = []
    #     variants_dict = {}
    #     script_tag = self.soup.find_all('script', id="back-in-stock-helper")[0]#.get_text().split("['inventory_quantity'] = ")[-1].replace(';', '').replace('\n', '')
    #     variant_id = self.soup.find_all('product-form', class_="product__block__buttons")[0].find('input', attrs={'type':'hidden', 'name':'id'}).get('value')
    #     product_id = self.soup.find_all('product-form', class_="product__block__buttons")[0].find('input', attrs={'type':'hidden', 'name':'product-id'}).get('value')
    #     section_id = self.soup.find_all('product-form', class_="product__block__buttons")[0].find('input', attrs={
    #         'type': 'hidden', 'name': 'section-id'}).get('value')
    #     variants_dict['cart'] = {'variant_id': variant_id, 'product_id': product_id, 'section_id': section_id}
    #     variants_dict['price'] = price_dict
    #     attributes_json = self.get_attributes_json()
    #     localisation_dict = {'срібло': 'silver', 'золото': 'gold'}
    #     print(333333, script_tag)

    #     if script_tag:
    #         script_content = script_tag.string
    #         pattern = re.findall(r"inventory_quantity\'\] = (\d+)", script_content)
    #         print(pattern, 11111111)
    #         for quantity in map(int, pattern):
    #             print(quantity, 222222)
    #             if quantity >= 1:
    #                 variants_dict['stock'] = {"status": "in_stock", "quantity": str(quantity)}
    #             else:
    #                 variants_dict['stock'] = {"status": "not_in_stock"}
    #
    #     for x in attributes_json:
    #         if not x['public_title']:
    #             color_name = self.soup.find_all('div', class_='product__media')[0].get('aria-label')
    #         else:
    #             color_name = x['public_title'].lower()
    #             if color_name in localisation_dict:
    #                 color_name = localisation_dict[color_name]
    #     variants_list.append(variants_dict)
    #     # variants_list.append({
    #     #     'cart': {'variant_id': variant_id, 'product_id': product_id, 'section_id': section_id},
    #     #     'price': price_dict,
    #     #     'selection': {'color': color_name},
    #     #     'stock': stock_dict,
    #     # })
    #     return variants_list

    def get_descr(self):
        return self.soup.find_all('div', class_='accordion-content__holder')[0].get_text().replace('\n', '').replace('  ', '')

    def get_assets(self):
        assets_list = []
        attributes_json = self.get_attributes_json()
        path = self.soup.find_all('div', class_='product__media')
        assets_dict = {}
        images_list = []
        videos_list = []
        if self.soup.find_all('div', class_='media__contain'): #.find('video').find('source').get('src'):
            video = self.soup.find_all('div', class_='media__contain')[0].find('video').find('source').get('src')
            videos_list.append({'url': video})
        for x in path:
            if x.get('data-type') == 'video':
                continue
            images = x.find('img').get('srcset')
            images_list.append({'url': images})
            for y in attributes_json:
                if not y['public_title']:
                    color_name = self.soup.find_all('div', class_='product__media')[0].get('aria-label')
                    assets_dict['selector'] = {'color': color_name}
                else:
                    assets_dict['selector'] = {}
            assets_dict['images'] = images_list
        assets_dict['videos'] = videos_list
        assets_list.append(assets_dict)
        return assets_list

    def get_attributes_json(self):
        scripts = self.soup.find_all("script")
        target_script = None
        for script in scripts:
            if script.string and "ShopifyAnalytics.meta" in script.string:
                target_script = script.string
                break
        if not target_script:
            print('Не знайдено потрібного скрипта')
        else:
            pattern = re.compile(r'"variants":(\[.*?\])', re.DOTALL)
            match = pattern.search(target_script)
            if match:
                variants_str = match.group(1)
                variants = json.loads(variants_str)
                return variants
            else:
                print('Не знайдено variants')

    def get_attributes(self):
        attributes_list = []
        attributes_dict = {}
        values_list = []
        attributes_dict['domainType'] = 'color'
        attributes_dict['id'] = 'color'
        attributes_dict['label'] = 'Color'
        rgb_dict = {'gold': '#D4AF37', 'silver': '#c0c0c0'}
        localisation_dict = {'срібло': 'silver', 'золото': 'gold'}
        attributes_json = self.get_attributes_json()
        for x in attributes_json:
            if not x['public_title']:
                color_name = self.soup.find_all('h1', class_="product__title heading-size-9")[0].get_text().replace(
                    '\n', '').replace('  ', '')
                values_list.append({'id': color_name, 'name': color_name, 'swatch': 'swatch'})
                attributes_dict['valueType'] = 'swatch'
            else:
                color_name = x['public_title'].lower()
                if color_name in localisation_dict:
                    color_name = localisation_dict[color_name]
                values_list.append({'id': color_name, 'name': color_name, 'rgb': rgb_dict[color_name]})

                attributes_dict['valueType'] = 'rgb'
            attributes_dict['values'] = values_list
        attributes_list.append(attributes_dict)
        return attributes_list



