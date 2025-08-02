from bs4 import BeautifulSoup
from lxml import etree
import requests
import os
import json
import redis

from read_data import FileConnector, RedisConnector, SQLiteConnector


class ContentFileNotExistError(Exception):
    pass


class Base:

    NAME = ''

    def __init__(self, page_link, force_from_page=False, storage='file'):
        self.force_from_page = force_from_page
        self.page_link = page_link
        self.file_name = self.get_file_name()
        self.storage = storage
        if storage == 'file':
            self.connector = FileConnector(self.NAME, self.file_name)
        elif storage == 'redis':
            self.connector = RedisConnector(self.NAME, self.file_name)
        elif storage == 'sqlite':
            self.connector = SQLiteConnector(self.NAME, self.file_name)
        else:
            raise NotImplementedError('not implemented storage {}'.format(storage))

    def run(self):
        self.avail_content = self.get_availability()
        if not self.connector.json_exist_in_storage() or not self.connector.json_exist_in_storage(json_type='full'):
            print('there is no data about product')
            self.connector.write_json_into_storage(self.avail_content)
            self.full_content = self.get_full()
            self.connector.write_json_into_storage(self.full_content, json_type='full')
            print('full and avail json were writtten into {}'.format(self.storage))
        else:
            print('full and avail json are already exist in {}, checking for inconsistent data'.format(self.storage))
            old_avail_json = self.connector.read_json_from_storage()
            if old_avail_json != self.avail_content:
                print('there are inconsistencies in availability json. updating avail json')
                self.connector.write_json_into_storage(self.avail_content)
                old_full_json = self.connector.read_json_from_storage(json_type='full')
                self.full_content = self.get_full()
                if self.check_attr_inconsistency(old_full_json, self.full_content):
                    self.connector.write_json_into_storage(self.full_content, json_type='full')

    def check_attr_inconsistency(self, old_full_json, new_full_json):
        # for x in old_full_json['product']['attributes']:
        #     for i in range(len(x['values'])):
        #         print(x['values'][i]['id'])
        return old_full_json['product']['attributes'] != new_full_json['product']['attributes']

    def get_file_name(self):
        return self.page_link.split('/')[-1].split('?')[0]

    def get_content(self, page_url, file_extention='txt', headers=None):
        file_path = 'temp_files/{}/{}/content_{}.{}'.format(self.NAME, self.file_name, self.file_name, file_extention)
        folder_name = r'temp_files/{}'.format(self.NAME)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        folder_name2 = r'temp_files/{}/{}'.format(self.NAME, self.file_name)
        if not os.path.exists(folder_name2):
            os.makedirs(folder_name2)
        if os.path.exists(file_path) and not self.force_from_page:
            with open(file_path, "r") as file1:
                content = file1.read()
        else:
            if headers:
                self.res = requests.get(page_url, headers=headers)
            else:
                self.res = requests.get(page_url)
            content = self.res.content.decode('utf-8')
            with open(file_path, "w") as file1:
                file1.write(content)
        return content

    def get_availability(self):
        brand_id = self.get_brand_id()
        store_id = self.get_store_id()
        product_id = self.get_store_id()
        availability_dict = {
            'extractedUrl': self.page_link,
            'hash': self.get_hash(store_id, product_id, brand_id),
            'product_id': product_id,
            'store_id': store_id,
            'variants': self.get_variants(),
        }
        return {'product': availability_dict}

    def get_full(self):
        product_id = self.get_product_id()
        store_id = self.get_store_id()
        variants = self.get_variants()
        attributes = self.get_attributes()
        assets = self.get_assets()
        brand_id = self.get_brand_id()
        breadcrumbs = self.get_breadcrumbs()
        description = self.get_descr()
        hash = self.get_hash(store_id, product_id, brand_id)
        if attributes:
            variantselectors = [x['id'] for x in attributes]
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
                'variantSelectors': variantselectors,
            }
        else:
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
                'variantSelectors': [],
            }
        return {'product': full_dict}

    def get_hash(self, store_id, product_id, brand):
        return hash((store_id, product_id, self.page_link, brand))

    def get_brand_id(self):
        raise NotImplementedError()

    def get_store_id(self):
        raise NotImplementedError()

    def get_product_id(self):
        raise NotImplementedError()

    def get_variants(self):
        raise NotImplementedError()

    def get_attributes(self):
        raise NotImplementedError()

    def get_assets(self):
        raise NotImplementedError()

    def get_breadcrumbs(self):
        raise NotImplementedError()

    def get_descr(self):
        raise NotImplementedError()


class BaseSoup(Base):
    def run(self):
        self.get_soup()
        super().run()

    def get_soup(self):
        self.soup = BeautifulSoup(self.get_content(self.page_link), 'html.parser')
        # html_text = soup.prettify()


class BaseLxml(Base):

    def run(self):
        self.get_tree()
        super().run()


    def get_tree(self):
        self.tree = etree.HTML(self.get_content(self.page_link))

