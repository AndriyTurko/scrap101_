#import requests
#from lxml import etree
import json
from base import BaseLxml


class Gorgany(BaseLxml):

    NAME = 'gorgany'

    def get_file_name(self):
        return self.page_link.replace('https://www.gorgany.com/', '')

    def get_json(self):
        div = self.tree.xpath("//div[@data-role='swatch-options']")[0]
        script_tag = div.getnext()
        json_text = script_tag.text
        json_text2 = json_text.replace('\n', '').replace(' ', '')
        dict_gs = json.loads(json_text2)
        return dict_gs

    def get_price(self):
        gj = self.get_json()['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']['jsonConfig']['optionPrices']
        for x in gj.values():
            regular_price = x['basePrice']
            fmp_price = x['oldPrice']
            price_dict = {"currency": "USD", "fmp": fmp_price, "regular": regular_price}
            return price_dict

    def get_name(self):
        return self.tree.xpath('//span[@itemprop="name"]')[0].text

    def get_descr(self):
        descr_text = self.tree.xpath('//div[@class="product attribute description"]/div[@class="value"]/p')[0].itertext()
        descr_l = ' '.join(descr_text)
        descr_end = (descr_l.replace("\xa0", "").replace('\n\t', '')
                     .replace('  ', ' ').replace(' .', '.'))
        return descr_end

    def get_brand_id(self):
        return self.tree.xpath('//div[@class="amshopby-option-link"]/a')[0].get('title')

    def get_store_id(self):
        return 'gorgany'

    def get_product_id(self):
        return self.get_json()['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']['jsonConfig']['productId']

    def get_breadcrumbs(self):
        breadcrumbs_list = []
        bread_path = self.tree.xpath('//div[@class="breadcrumbs"]//li//a')
        for x in bread_path:
            a = x.text.replace(' ', '').replace('\n', '')
            breadcrumbs_list.append(a)
        b = self.tree.xpath('//div[@class="breadcrumbs"]//li//strong')[0].text
        breadcrumbs_list.append(b)
        return breadcrumbs_list

    def get_attributes(self):
        attributes_list = []
        gj = self.get_json()['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']['jsonConfig']
        for x in gj['attributes'].values():
            attributes_dict = {}
            attributes_dict['domainType'] = x['code']
            attributes_dict['id'] = x['id']
            attributes_dict['label'] = x['label']
            values_list = []
            for q in x['options']:
                if x['code'] == 'color':
                    attributes_dict['valueType'] = 'swatch'
                    values_list.append({'id': q['id'], 'label': q['label'], 'swatch': 'a'})
                else:
                    attributes_dict['valueType'] = 'string'
                    values_list.append({'id': q['id'], 'label': q['label']})
                attributes_dict['values'] = values_list
            attributes_list.append(attributes_dict)
        return attributes_list

    def get_variants(self):
        return []

    def get_assets(self):
        return []

    def get_photo(self, g_json):
        asset_names = {'93': 'color', '168': 'size'}
        attributes_data = g_json['[data-role=swatch-options]']["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]['attributes']
        new_attribute_data = {}
        for attribute_id in attributes_data:
            attr_dict = {}
            for attr_data2 in attributes_data[attribute_id]['options']:
                attr_dict[attr_data2['id']] = attr_data2['label']
            new_attribute_data[attribute_id] = attr_dict
        print(json.dumps(new_attribute_data))
        images_data = g_json['[data-role=swatch-options]']["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]['images']
        index_data = g_json['[data-role=swatch-options]']["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]['index']
        # print(json.dumps(index_data))
        # print(json.dumps(attributes_data))
        # print(json.dumps(images_data))
        assets_list = []
        for asset_id in index_data:
            assets_dict = {}
            print(asset_id)
            images_list = []
            for images_data2 in images_data[asset_id]:
                images_list.append({'url': images_data2['full']})
            #print(images_list)
            assets_dict['images'] = images_list
            selector_dict = {}
            for selector_type in index_data[asset_id]:
                swatch_id = index_data[asset_id][selector_type]
                swatch_type = asset_names[selector_type]
                selector_dict[swatch_type] = new_attribute_data[selector_type][swatch_id]
            assets_dict['selector'] = selector_dict
            assets_list.append(assets_dict)
        return assets_list

