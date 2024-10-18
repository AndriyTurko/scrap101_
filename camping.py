import requests
from lxml import etree
import json


class Camping:
    def __init__(self, page_link):
        self.page_link = page_link
        self.tree = self.get_tree()

    def get_tree(self):
        res = requests.get(self.page_link)
        tree = etree.HTML(res.content)
        return tree

    def get_json(self):
        div = self.tree.xpath('//script')[0]
        json_text = div.text
        json_text2 = json_text.strip().strip('//<!--\n    var data = ').strip(';    //-->')
        dict_gs = json.loads(json_text2)
        return dict_gs

    def get_price(self):
        price_list = self.tree.xpath('//span[@id="priceSellingVat"]')
        print(price_list)
        price = price_list[0].text
        price_int = int(price.replace(u"\xa0", u"").replace('грн', '').replace('\n', '').replace('від', '').replace('   ', '').replace(' ', ''))
        return price_int

    def get_variants2(self):
        variants_list = []
        if 'variantsInfo' in self.get_json():
            variants_info_data = self.get_json()['variantsInfo']
            for variant_dict in variants_info_data:
                split_name = variants_info_data[variant_dict]['name'].split('/')
                selection_dict = {}
                for split_variant in split_name:
                    split_name2 = split_variant.split(':')
                    split_name3 = split_name2[1].replace(' ', '')
                    key_name = split_name2[0].strip()
                    if key_name in ['Розмір взуття (EU)', 'Розмір']:
                        key_name = 'size'
                    elif key_name == 'Колір':
                        key_name = 'color'
                    elif key_name == 'Блискавка':
                        key_name = 'zip'
                    selection_dict[key_name] = split_name3
                regular_price = variants_info_data[variant_dict]['price']
                fmp_price = variants_info_data[variant_dict]['priceOld']
                price_dict = {'regular': regular_price, 'fmp': fmp_price, 'currency': 'UAH'}
                id_dict = variants_info_data[variant_dict]['id']
                availability = variants_info_data[variant_dict]['availability']
                stock_dict = {'status': availability}
                variants_list.append({
                    'price': price_dict,
                    'selection': selection_dict,
                    'id': id_dict,
                    'stock': stock_dict,
                })
            return variants_list
        else:
            return []

    def get_name(self):
        name_l = self.tree.xpath('//div[@class="product-heading-block row-fluid"]/h1')
        print(name_l)
        name = name_l[0].text.strip()
        return name

    def get_descr(self):
        descr_l = self.tree.xpath('//div[@class="truncated-content-inner"]')
        print(descr_l)
        descr = descr_l[0].itertext()
        print(descr)
        descr_l = ' '.join(descr)
        descr_end = descr_l.replace("\xa0", "").replace('\n\t', '').replace('  ', ' ').replace(' .', '.').replace('\n', '').replace(' , ', ', ').replace('.  ', '. ').replace('  ', '').replace('.', '. ')
        return descr_end

    def get_brand(self):
        brand_l = self.tree.xpath('//p[@class="product-producer-logo"]//img')
        print(brand_l)
        brand_ex = brand_l[0]
        brand = brand_ex.get('alt')
        return brand

    def get_breadcrumbs(self):
        bread_l = self.tree.xpath("//ul[@class='breadcrumb']/li/a/span")
        print(bread_l)
        breadcrumbs = []
        for x in bread_l:
            breadcrumbs.append(x.text)
        return breadcrumbs

    # def get_variants(self, g_json):
    #     assets_name = {'74': 'size', '23': 'color'}
    #     variants_list = []
    #     if 'variantsInfo' in g_json:
    #         variants_info_data = g_json['variantsInfo']
    #         index_data = g_json['variantsTree']
    #         for size in index_data:
    #             for color in index_data[size]:
    #                 print(color)
    #                 print(index_data[size][color])
    #                 for x in variants_info_data:
    #                     print(x)
    #         return variants_list

    def get_photos(self):
        photos_list = []
        photos_l = self.tree.xpath('//ul[@id="additionalImages"]//li')
        if photos_l:
            for x in photos_l:
                a = x.xpath('.//a')
                if len(a) == 0:
                    continue
                b = a[0].get('href')
                url_dict = {'url': b}
                photos_list.append(url_dict)
        else:
            photos_l2 = self.tree.xpath('//img')[0]
            photo = photos_l2.get('src')
            url_dict = {'url': photo}
            photos_list.append(url_dict)
        return photos_list

    def get_video(self):
        videos_list = []
        videos_l = self.tree.xpath('//div[@id="productVideoSection"]//iframe')
        for x in videos_l:
            video = x.get('src')
            url_dict = {'url': video}
            videos_list.append(url_dict)
        return videos_list

    def get_domain_type(self, control_group):
        following_button = control_group.xpath("./following-sibling::button")
        if following_button:
            button_id = following_button[0].get('id')
            domain_type = button_id.replace('IdButton', '')
            return domain_type
        else:
            following_div = control_group.xpath('./following-sibling::div[@class="variant-options"]')
            div_id = following_div[0].get('id')
            domain_type = div_id.replace('variant', '').replace('Options', '')
            return domain_type.lower()

    def get_attributes(self):
        attributests_list = []
        variant_selectors_list = []
        attributests_l = self.tree.xpath('//fieldset[@id="variants"]')
        print(attributests_l)
        if len(attributests_l) >= 1:
            control_group_l = attributests_l[0].xpath('.//div[@class="control-group"]')
            for x in control_group_l:
                attr_dict = {}
                domain_type = self.get_domain_type(x)
                attr_dict['domainType'] = domain_type
                control_label = x.xpath('.//label[@class="control-label"]')[0]
                label = control_label.text
                attr_id = control_label.get('for').replace('id_', '')
                swatch_l = attributests_l[0].xpath('.//div[@id="variantColourOptions"]')
                attr_dict['label'] = label
                attr_dict['id'] = attr_id
                attr_dict['valueType'] = 'swatch'
                values_list = []
                for y in x.xpath('.//option'):
                    attr_id2 = y.get('value')
                    attr_name = y.text
                    for x in swatch_l:
                        control_swatch = x.xpath('.//source')[0]
                        swatch = control_swatch.get('srcset')
                        values_list.append({'id': attr_id2, 'name': attr_name, 'swatch': swatch})
                    attr_dict['values'] = values_list
                variant_selectors_list.append(domain_type)
                attributests_list.append(attr_dict)
        return attributests_list, variant_selectors_list

    def get_hash(self, store_id, product_id, brand):
        return hash((store_id, product_id, self.page_link, brand))

    def get_assets(self):
        assets_list = []
        assets_dict = {}
        assets_dict['images'] = self.get_photos()
        assets_dict['videos'] = self.get_video()
        #assets_list['selector'] = self.
        assets_list.append((assets_dict))
        return assets_list

    def get_full(self):
        product_json = self.get_json()
        product_id = product_json['productId']
        store_id = '4camping'
        variants = self.get_variants2()
        assets = self.get_assets()
        attributes, variant_selectors_list = self.get_attributes()
        brand_id = self.get_brand()
        breadcrumbs = self.get_breadcrumbs()
        description = self.get_descr()
        hash = self.get_hash(store_id, product_id, brand_id)
        full_dict = {
            'extractedUrl': self.page_link,
            'hash': hash,
            'product_id': product_id,
            'store_id': store_id,
            'variants': variants,
            'assets': assets,
            'attributes': attributes,
            'brand': brand_id,
            'category': breadcrumbs,
            'description': description,
            'variantSelectors': variant_selectors_list,
        }
        return {'product': full_dict}

    def get_availability(self):
        product_json = self.get_json()
        brand_id = self.get_brand()
        product_id = product_json['productId']
        store_id = '4camping'
        variants = self.get_variants2()
        hash = self.get_hash(store_id, product_id, brand_id)
        availability_dict = {
            'extractedUrl': self.page_link,
            'hash': hash,
            'product_id': product_id,
            'store_id': store_id,
            'variants': variants,
        }
        return {'product': availability_dict}