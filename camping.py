from base import BaseLxml
import json


class Camping(BaseLxml):

    NAME = 'camping'

    def __init__(self, page_link, force_from_page=False):
        super().__init__(page_link, force_from_page=force_from_page)

    def get_file_name(self):
        return self.page_link.replace('https://4camping.com.ua/p/', '').replace('/', '')

    def get_json(self):
        div = self.tree.xpath('//script')[0]
        json_text = div.text
        json_text2 = json_text.strip().strip('//<!--\n    var data = ').strip(';    //-->')
        dict_gs = json.loads(json_text2)
        return dict_gs


    def get_price2(self, variant_dict):
        regular_price = variant_dict['price']
        fmp_price = variant_dict['priceOld']
        price_dict = {'regular': regular_price, 'fmp': fmp_price, 'currency': 'UAH'}
        message_price = variant_dict['priceWithDiscountFormatted']
        message_price_int = int(message_price.replace('&nbsp;', '').replace('<span class="currency">грн</span>', ''))
        if message_price_int != regular_price:
            price_dict['message'] = str(message_price_int) + ' грн для членів 4camping eXtra'
        return price_dict

    def get_variants(self):
        variants_list = []
        if 'variantsInfo' in self.get_json():
            variants_info_data = self.get_json()['variantsInfo']
            for variant_dict in variants_info_data.values():
                price_dict = self.get_price2(variant_dict)
                id_dict = variant_dict['id']
                availability = variant_dict['availability']
                if availability == 'На складі':
                    stock_dict = {'status': 'in_stock'}
                else:
                    stock_dict = {'status': 'in_stock', 'message': availability}
                cart_id = variant_dict['productId']
                cart_dict = {"id": cart_id, "variant": id_dict}
                variants_list.append({
                    'cart': cart_dict,
                    'price': price_dict,
                    'selection': variant_dict['params'],
                    'id': id_dict,
                    'stock': stock_dict,
                })
            return variants_list
        else:
            return []

    def get_name(self):
        name_l = self.tree.xpath('//div[@class="product-heading-block row-fluid"]/h1')
        name = name_l[0].text.strip()
        return name

    def get_descr(self):
        descr_l = self.tree.xpath('//div[@class="truncated-content-inner"]')
        descr = descr_l[0].itertext()
        descr_l = ' '.join(descr)
        descr_end = descr_l.replace("\xa0", "").replace('\n\t', '').replace('  ', ' ').replace(' .', '.').replace('\n', '').replace(' , ', ', ').replace('.  ', '. ').replace('  ', '').replace('.', '. ')
        return descr_end

    def get_brand(self):
        brand= self.tree.xpath('//p[@class="product-producer-logo"]//img')[0].get('alt')
        return brand

    def get_breadcrumbs(self):
        bread_l = self.tree.xpath("//ul[@class='breadcrumb']/li/a/span")
        breadcrumbs = []
        for x in bread_l:
            breadcrumbs.append(x.text)
        return breadcrumbs

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
        # TODO 6. Робити в останню чергу - пишу щоб не забути.
        #  для товарів де немає 'color' або 'size' для якогось атрибуту написати 'domainType: 'fit'
        #  (приклад https://4camping.com.ua/p/pinguin-safari/)
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
        attributests_l = self.tree.xpath('//fieldset[@id="variants"]')
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
                attributests_list.append(attr_dict)
        return attributests_list

    def get_assets(self):
        assets_list = []
        assets_dict = {}
        assets_dict['images'] = self.get_photos()
        assets_dict['videos'] = self.get_video()
        assets_list.append((assets_dict))
        return assets_list

    def get_brand_id(self):
        return self.get_brand()

    def get_store_id(self):
        return 'camping'

    def get_product_id(self):
        return self.get_json()['productId']

