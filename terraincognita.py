#from lxml import etree
import json
from base import BaseLxml


class Terra(BaseLxml):

    NAME = 'terraincognita'

    def get_file_name(self):
        file_name = self.page_link.replace('https://terraincognita.com.ua/', '').replace('/', '')
        return file_name

    def get_json_variants(self):
        div = self.tree.xpath('//div[@class="product__options product__page-options"]')
        if div:
            json_text = div[0].getnext().text
            json_text2 = json_text.strip().strip('//<!--\n    var data = ').strip(';    //-->')
            json_text3 = json_text2.replace('let ro_variants = ', '')
            dict_gs = json.loads(json_text3)
            return dict_gs

    def get_hash(self, store_id, product_id, brand):
        return hash((store_id, product_id, self.page_link, brand))

    def get_brand(self):
        brand = self.tree.xpath('//span[@itemprop="name"]')[0].text
        return brand

    def _get_stock_message(self, city_stock):
        city_stock_msg = 'Quantity by city: '
        for k, v in city_stock.items():
            if int(v) != 0:
                city_stock_msg += k + ': ' + v + '; '
        return city_stock_msg

    def get_variants(self):
        variants_list = []
        gjv = self.get_json_variants()
        if gjv is not None:
            for x in gjv:
                if gjv[x]['quantity'] == '0':
                    pass
                else:
                    price_dict = self.get_price(gjv[x])
                    selection_dict = {}
                    cart_dict = {}
                    options_dict = {}
                    option_list = []
                    for params in gjv[x]['params']:
                        selection = params.split('_')
                        selection_dict[selection[0]] = selection[1]
                        option_path_one = '//ul[@data-option-id="' + selection[0] + '"]'
                        option_el_one = self.tree.xpath(option_path_one)[0].get('data-product-option-id')
                        option_path_two = '//li[@data-option-value-id="' + selection[1] + '"]'
                        option_el_two = self.tree.xpath(option_path_two)[0].get('data-product-option-value-id')
                        options_dict[option_el_one] = option_el_two
                        option = '<span>' + gjv[x]['params'][params]['name'] + '</span>: ' + gjv[x]['params'][params]['value']
                        option_list.append(option)
                    cart_dict['options'] = options_dict
                    product_id = self.tree.xpath('//input[@name="product_id"]')[0].get('value')
                    cart_dict['product_id'] = product_id
                    cart_dict['sku'] = gjv[x]['sku']
                    cart_dict['option'] = '<br>'.join(option_list)
                    availability = int(gjv[x]['quantity'])
                    stock_dict = {
                        'status': 'in_stock',
                        'quantity': availability,
                        'message': self._get_stock_message(gjv[x]['quantity_by_city'])
                    }
                    variants_list.append({
                        'cart': cart_dict,
                        'id': x,
                        'price': price_dict,
                        'selection': selection_dict,
                        'sku': gjv[x]['sku'],
                        'stock': stock_dict,
                    })
            return variants_list
        else:
            regular_price = self.tree.xpath('//span[@class="price-new"]//span')[0].get('content')
            fmp_price = self.tree.xpath('//div[@class="old_price-wrap"]//span')[0].get('content')
            if not fmp_price:
                fmp_price = regular_price
            price_dict = {
                'regular': regular_price,
                'fmp_price': fmp_price,
                'currency': 'UAH'
            }
            cart_dict = {}
            product_id = self.tree.xpath('//input[@name="product_id"]')[0].get('value')
            cart_dict['product_id'] = product_id
            stock_dict = {}
            quantity_path = self.tree.xpath('//div[@class="stock_in_store"]//li')
            quantity = 0
            quantity_message = {}
            for x in quantity_path:
                place = ''.join(x.itertext()).replace('\n\t\t\t\t\t\t\t\t', '').replace(' ', '')
                quantity_by_city = int(x.get('data-quantity'))
                stock_dict['status'] = 'in_stock'
                quantity += quantity_by_city
                stock_dict['quantity'] = quantity
                quantity_message[place] = quantity_by_city
                stock_dict['message'] = quantity_message
            variants_list.append({
                'cart': cart_dict,
                'price': price_dict,
                'stock': stock_dict,
            })
            return variants_list

    def get_price(self, x):
        fmp_price = float(x['price'].replace('<span>₴</span>', '').replace(' ', ''))
        if not x['special']:
            regular_price = fmp_price
        else:
            regular_price = float(x['special'].replace('<span>₴</span>', ''))
        price_dict = {'regular': regular_price, 'fmp': fmp_price, 'currency': 'UAH'}
        return price_dict

    def get_name(self):
        name = self.tree.xpath('//h1[@itemprop="name"]')[0].text
        return name

    def get_descr(self):
        descr = self.tree.xpath('//div[@id="collapse-description"]//p')
        if descr:
            descr = self.tree.xpath('//div[@id="collapse-description"]//p')[0].text
            return descr
        else:
            descr_2 = self.tree.xpath('//div[@id="collapse-description"]//div')[0].text
            return descr_2

    def get_breadcrumbs(self):
        bread_list = []
        bread = self.tree.xpath('//ul[@class="breadcrumb"]//li/a')
        for x in bread[1:]:
            bread_list.append(x.text)
        return bread_list

    def get_attributes(self):
        attributests_list = []
        attributests_l = self.tree.xpath('//div[@class="product__page-option_wrap"]')
        for x in attributests_l:
            attr_dict = {}
            label = x.xpath('.//span[@class="product__page-options_title"]')[0].text.replace(' (спершу оберіть колір) ', '').replace(' ', '')
            id = x.xpath('.//ul')[0].get('data-option-id')
            attr_dict['id'] = id
            attr_dict['label'] = label
            if label == 'Колір':
                domain_type = 'color'
            elif label == 'Розмір':
                domain_type = 'size'
            else:
                domain_type = 'fit'
            attr_dict['domainType'] = domain_type
            values_list = []
            for y in x.xpath('.//ul//li'):
                id = y.get('data-option-value-id')
                attr_name = y.get('data-name')
                swatch_l = y.xpath('.//img[@class="option__img"]')
                if swatch_l:
                    swatch = swatch_l[0].get('src')
                    values_list.append({'id': id, 'name': attr_name, 'swatch': swatch})
                    attr_dict['valueType'] = 'swatch'
                else:
                    values_list.append({'id': id, 'name': attr_name})
                    attr_dict['valueType'] = 'string'
                attr_dict['values'] = values_list
            attributests_list.append(attr_dict)
        return attributests_list

    def get_photos(self):
        photos_l = self.tree.xpath('//div[@class="thumb-vertical-outer"]//li')
        photos_dict = {}
        for p in photos_l:
            photo = p.xpath('.//img')[0].get('data-src')
            color_id = p.get('data-option-value')
            if color_id not in photos_dict:
                photos_dict[color_id] = [photo]
            else:
                photos_dict[color_id].append(photo)
        return photos_dict

    def get_videos(self):
        videos_list = []
        videos_l = self.tree.xpath('//div[@class="tab-content  col-xs-12"]//iframe')
        if videos_l:
            video = videos_l[0].get('src')
            url_dict = {'url': video}
            videos_list.append(url_dict)
        return videos_list

    def get_assets(self, attributes):
        photos_dict = self.get_photos()
        assets_list = []
        videos = self.get_videos()
        values = None
        for attrib in attributes:
            if attrib['domainType'] == 'color':
                values = attrib['values']
                break
        if values:
            for v in values:
                color_id = v['id']
                images_list = photos_dict.get(color_id, [])
                if '0' in photos_dict:
                    images_list.extend(photos_dict['0'])
                if '' in photos_dict:
                    images_list.extend(photos_dict[''])
                assets_list.append({
                    'images': images_list,
                    'selector': {'color': color_id},
                    'videos': videos,
                })
        else:
            images_list = []
            if '0' in photos_dict:
                images_list.extend(photos_dict['0'])
            if '' in photos_dict:
                images_list.extend(photos_dict[''])
            assets_list.append({
                'images': images_list,
                'selector': {},
                'videos': videos,
            })
        return assets_list

    # def get_assets(self, attributes):
    #     assets_list = []
    #     videos = self.get_videos()
    #     values = None
    #     for attrib in attributes:
    #         if attrib['domainType'] == 'color':
    #             values = attrib['values']
    #             break
    #     if values:
    #         for v in values:
    #             color_id = v['id']
    #             photo_path = '//li[@data-option-value="' + color_id + '"]//img'
    #             images = [x.get('data-src') for x in self.tree.xpath(photo_path)]
    #             assets_list.append({
    #                 'images': images,
    #                 'selector': {'color': color_id},
    #                 'videos': videos,
    #             })
    #             for x in self.tree.xpath('//ul[@class="thumb-vertical"]//li'):
    #                 color_ids_ex = x.get('data-option-value')
    #                 if color_ids_ex == '0':
    #                     extra_photo = self.tree.xpath('//li[@data-option-value="0"]//img')[0].get('data-src')
    #                     images.append(extra_photo)
    #     else:
    #         images = [x.get('data-src') for x in self.tree.xpath('//div[@id="thumb-slider"]//img')]
    #         assets_list.append({
    #             'images': images,
    #             'selector': {},
    #             'videos': videos,
    #         })
    #     return assets_list

    def get_availability(self):
        brand_id = self.get_brand()
        store_id = 'terraincognita'
        product_id = self.tree.xpath('//input[@name="product_id"]')[0].get('value')
        hash = self.get_hash(store_id, product_id, brand_id)
        variant = self.get_variants()
        availability_dict = {
            'extractedUrl': self.page_link,
            'hash': hash,
            'product_id': product_id,
            'store_id': store_id,
            'variants': variant,
        }
        return {'product': availability_dict}

    def get_full(self):
        product_id = self.tree.xpath('//input[@name="product_id"]')[0].get('value')
        store_id = 'terraincognita'
        variants = self.get_variants()
        attributes = self.get_attributes()
        assets = self.get_assets(self.get_attributes())
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
            'variantSelectors': 'variant_selectors_list',
        }
        return {'product': full_dict}