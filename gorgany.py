#import requests
#from lxml import etree
import json
from base import BaseLxml


class Gorgany(BaseLxml):

    NAME = 'gorgany'

    def get_file_name(self):
        return self.page_link.split('/')[-1]

    def get_json(self):
        div = self.tree.xpath("//div[@data-role='swatch-options']")
        if div:
            script_tag = div[0].getnext()
            json_text = script_tag.text
            json_text2 = json_text.replace('\n', '').replace(' ', '')
            dict_gs = json.loads(json_text2)
            return dict_gs

    def get_price(self):
        if self.get_json():
            gj = self.get_json()['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']['jsonConfig']['optionPrices']
            for x in gj.values():
                regular_price = x['basePrice']['amount']
                fmp_price = x['oldPrice']['amount']
                price_dict = {"currency": "USD", "fmp": fmp_price, "regular": regular_price}
                return price_dict
        else:
            json_text = self.tree.xpath('//script[@type="application/ld+json"]')[-1].text
            json_text2 = json_text.replace('\n', '')
            dict_gs = json.loads(json_text2)
            currency = dict_gs['offers']['priceCurrency']
            regular_price = dict_gs['offers']['price']
            price_dict = {"currency": currency, "fmp": regular_price, "regular": regular_price}
            return price_dict, dict_gs

    def get_name(self):
        return self.tree.xpath('//span[@itemprop="name"]')[0].text

    def get_descr(self):
        descr_text = self.tree.xpath('//div[@class="product attribute description"]/div[@class="value"]')[0].itertext()
        descr_l = ' '.join(descr_text)
        descr_end = (descr_l.replace("\xa0", "").replace('\n\t', '')
                     .replace('  ', ' ').replace(' .', '.'))
        return descr_end

    def get_brand_id(self):
        return self.tree.xpath('//div[@class="amshopby-option-link"]/a')[0].get('title')

    def get_store_id(self):
        return 'gorgany'

    def get_product_id(self):
        if self.get_json():
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
        if self.get_json():
            gj = self.get_json()['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']
            swatch_ids = [s for s in gj['jsonSwatchConfig']['93']]
            for x in gj['jsonConfig']['attributes'].values():
                attributes_dict = {}
                attributes_dict['domainType'] = x['code']
                attributes_dict['id'] = x['id']
                attributes_dict['label'] = x['label']
                values_list = []
                for q in x['options']:
                    if x['code'] == 'color' and q['id'] in swatch_ids:
                        attributes_dict['valueType'] = 'swatch'
                        values_list.append({'id': q['id'], 'name': q['label'], 'swatch': gj['jsonSwatchConfig']['93'][q['id']]['value']})
                    else:
                        attributes_dict['valueType'] = 'string'
                        values_list.append({'id': q['id'], 'name': q['label']})
                    attributes_dict['values'] = values_list
                attributes_list.append(attributes_dict)
        return attributes_list

    def get_variants(self):
        variants_list = []
        if self.get_json():
            gj = self.get_json()['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']['jsonConfig']
            price_dict = self.get_price()
            for x in gj['index']:
                selection_dict = gj['index'][x]
                sku = gj['sku'][x]
                variants_list.append({
                    'cart': {'id': sku},
                    'id': x,
                    'price': price_dict,
                    'selection': selection_dict,
                    'stock': {'status': 'in_stock'},
                })
            return variants_list
        else:
            gj = self.get_price()[1]
            price_dict = self.get_price()[0]
            sku = gj['sku']
            variants_list.append({
                'price': price_dict,
                'sku': sku,
            })
            return variants_list

    def get_assets(self):
        assets_list = []
        if self.get_json():
            gj = self.get_json()['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']
            swatch_dict = self.get_swatches_for_assets(gj)
            for ind in gj['jsonConfig']['images']:
                assets_dict = {}
                images_list = []
                videos_list = []
                assets_dict['selector'] = gj['jsonConfig']['index'][ind]
                for im in gj['jsonConfig']['images'][ind]:
                    images = im['full']
                    images_list.append({'url': images})
                    assets_dict['images'] = images_list
                    assets_dict['videos'] = videos_list
                selection_color = assets_dict['selector']['93']
                swatch_link = swatch_dict['93'][selection_color]
                assets_dict['images'].append({'url': swatch_link})
                assets_list.append(assets_dict)
            return assets_list
        else:
            image_1 = self.tree.xpath('//div[@id="gallery-placeholder-image"]//source')
            image_2 = self.tree.xpath('//meta[@property="og:image"]')
            if image_1 and image_2:
                for x in image_1[0].get('srcset'), image_2[0].get('content'):
                    assets_dict = {}
                    images_list = []
                    videos_list = []
                    images_list.append({'url': x})
                    assets_dict['images'] = images_list
                    assets_dict['videos'] = videos_list
                    assets_list.append(assets_dict)
            return assets_list


    def get_swatches_for_assets(self, data_json):
        swatch_dict = {}
        swatch_json = data_json['jsonSwatchConfig']['93']
        for x in swatch_json:
            if isinstance(swatch_json[x], dict) and swatch_json[x].get('type') == 2:
                swatch_dict[x] = swatch_json[x].get('value')
        return {'93': swatch_dict}



