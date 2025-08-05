import json
import os
import requests

from base import BaseLxml


class Backcountry(BaseLxml):

    NAME = 'backcountry'

    def __init__(self, page_link, force_from_page=False):
        super().__init__(page_link, force_from_page)
        self.json = None
        self.bread_crumb_json = None

    def get_tree(self):
        super().get_tree()
        self.get_json()

    def get_content(self, page_url, file_extention='txt'):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        return super().get_content(page_url, file_extention, headers)

    def get_json(self):
        js_sc = self.tree.xpath('//script[@type="application/ld+json"]')
        print(js_sc)
        self.json = json.loads(js_sc[1].text)
        self.bread_crumb_json = json.loads(js_sc[0].text)

    def get_brand_id(self):
        return self.json["brand"]["name"]

    def get_store_id(self):
        return self.NAME

    def get_product_id(self):
        return self.json["sku"]

    def get_variants(self):
        variants_list = []
        for variant in self.json["hasVariant"]:
            sku = self.get_product_id()
            cart_dict = {
                "productId": self.json["sku"],
                "skuId": sku
            }
            selection_dict = {"color": variant.get("color", ""), "size": variant.get("size", "")}
            #fmp_price =
            price_dict = {
                "currency": variant["offers"]["priceCurrency"],
                "regular": variant["offers"]["price"],
                "fmp": variant["offers"]["price"]
            }
            variants_list.append({
                "cart": cart_dict,
                "id": sku,
                "price": price_dict,
                "selection": selection_dict,
                "sku": sku,
                "stock": {"status": "in_stock"}
            })
        return variants_list

    def get_attributes(self):
        attributests_list = []
        color_attrs = self.get_colors()
        if color_attrs:
            attributests_list.append(color_attrs)

        size_attrs = self.get_sizes()
        if size_attrs:
            attributests_list.append(size_attrs)

        return attributests_list

    def get_colors(self):
        color_block = self.tree.xpath('//div[@data-id="colorTile"]')[0]
        if not color_block:
            return

        color_values = []

        for color_element in color_block.xpath('.//div[@data-id="color-available"]/img'):
            color = color_element.get("alt")
            color_values.append({
                "id": color,
                "color": color,
                "swatch": color_element.get("src")
            })

        return {
            "domainType": "color",
            "id": "color",
            "label": "Color",
            "valueType": "swatch",
            "values": color_values
        }

    def get_sizes(self):
        size_block = self.tree.xpath('//div[@data-id="sizeTile"]')[0]
        if not size_block:
            return

        size_values = []

        ex = list(dict.fromkeys([x.text for x in size_block.xpath('.//span')]))
        for size in ex:
            size_values.append({
                "id": size,
                "color": size
            })

        return {
            "domainType": "size",
            "id": "size",
            "label": "Size",
            "valueType": "string",
            "values": size_values
        }

    def get_assets(self):
        assets_list = []
        assets_dict = {}
        #path = self.tree.xpath('//button[@class="chakra-button css-18lzhd2"]')
        a_json = self.tree.xpath('//script[@type="application/json"]')[0].text
        print(a_json)
        return assets_list

    def get_breadcrumbs(self):
        bredcrumbs = []
        for category in self.bread_crumb_json["itemListElement"]:
            bredcrumbs.append(category["name"])

        return bredcrumbs

    def get_descr(self):
        return self.json["description"]