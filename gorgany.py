import requests
from lxml import etree
import json


def get_tree(page_link):
    res = requests.get(page_link)
    tree = etree.HTML(res.content)
    return tree


def get_json(tree):
    div = tree.xpath("//div[@data-role='swatch-options']")[0]
    script_tag = div.getnext()
    json_text = script_tag.text
    json_text2 = json_text.replace('\n', '').replace(' ', '')
    dict_gs = json.loads(json_text2)
    return dict_gs
    
    
def get_price1(tree):
    price_list = tree.xpath('//span[@class="price"]')
    print(price_list)
    price = price_list[0].text
    price_int = int(price.replace(u"\xa0", u"").replace('грн', ''))
    return price_int


def get_price2(tree):
    price_l = tree.xpath('//span[@class="price-wrapper "]')
    print(price_l)
    print('--------------')
    price = price_l[0]
    q = price.get('data-price-amount')
    w = int(q)
    print(w)
    print('---------------')
    return w


def get_name(tree):
    name_l = tree.xpath('//span[@itemprop="name"]')
    print(name_l)
    name = name_l[0].text
    return name


def get_descr(tree):
    descr_l = tree.xpath('//div[@class="product attribute description"]/div[@class="value"]/p')
    print(descr_l)
    descr = descr_l[0].itertext()
    print(descr)
    descr_l = ' '.join(descr)
    descr_end = descr_l.replace("\xa0", "").replace('\n\t', '').replace('  ', ' ').replace(' .', '.')
    return descr_end


def get_descr2(tree):
    descr_l = tree.xpath('//div[@class="product attribute description"]/div[@class="value"]/p')
    print(descr_l)
    descr = descr_l[0].itertext()
    descr_list = []
    for descr_line in descr:
        print(descr_line)
#        descr_line2 = descr_line.replace('\xa0', '').replace('\n\t', '').replace('  ', ' ').replace(' .', '.')
        descr_line2 = descr_line.strip()
        descr_list.append(descr_line2)
    print(descr_list)
    descr_end = ' '.join(descr_list)
    return descr_end


def get_brand(tree):
#    brand_l = tree.xpath('//div[@class="amshopby-option-link"]/a')
#    brand2 = tree.xpath('//div[@class="amshopby-option-link"]')
#    brand_l = brand2[0].xpath('./a')
    brand_l = tree.xpath('//div[@class="amshopby-option-link"]//img')
    print(brand_l)
    brand_ex = brand_l[0]
    brand = brand_ex.get('title')
    return brand


def get_size(g_json):
    swatch_data = g_json['[data-role=swatch-options]']["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]["attributes"]
    size_list = []
    if '168' in swatch_data:
        size_data = swatch_data['168']['options']
        print(size_data)
        for x in size_data:
            size_list.append(x['label'])
    return size_list


# print(dict_gs['[data-role=swatch-options]']["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]["attributes"]["168"]["options"][1]["label"])


def get_breadcrumbs(tree):
    bread_l = tree.xpath("//div[@class='breadcrumbs']//li/a")
    print(bread_l)
    breadcrumbs = []
    for x in bread_l:
        breadcrumbs.append(x.text.strip())
    return breadcrumbs


def get_color(g_json):
    swatch_data = g_json['[data-role=swatch-options]']["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]["attributes"]
    color_list = []
    if '93' in swatch_data:
        color_data = swatch_data['93']['options']
        for x in color_data:
            color_list.append(x['label'])
    return color_list


def get_photo(g_json):
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

