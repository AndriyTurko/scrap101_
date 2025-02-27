from bs4 import BeautifulSoup
from lxml import etree
import requests
import os
import json


class ContentFileNotExistError(Exception):
    pass


class Base:

    NAME = ''

    def __init__(self, page_link, force_from_page=False):
        self.force_from_page = force_from_page
        self.page_link = page_link

    def run(self):
        full_content = self.get_full()
        avail_content = self.get_availability()
        file_path_avail = 'temp_files/{}/{}/avail_{}.json'.format(self.NAME, self.get_file_name(), self.get_file_name())
        file_path_full = 'temp_files/{}/{}/full_{}.json'.format(self.NAME, self.get_file_name(), self.get_file_name())
        with open(file_path_avail, "w") as file1:
            file1.write(json.dumps(avail_content))
        with open(file_path_full, "w") as file1:
            file1.write(json.dumps(full_content))


    def get_file_name(self):
        raise NotImplementedError()

    def get_content(self, page_url, file_extention='txt'):
        file_path = 'temp_files/{}/{}/content_{}.{}'.format(self.NAME, self.get_file_name(), self.get_file_name(), file_extention)
        folder_name = r'temp_files/{}'.format(self.NAME)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        folder_name2 = r'temp_files/{}/{}'.format(self.NAME, self.get_file_name())
        if not os.path.exists(folder_name2):
            os.makedirs(folder_name2)
        if os.path.exists(file_path) and not self.force_from_page:
            with open(file_path, "r") as file1:
                content = file1.read()
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
    def __init__(self, page_link, force_from_page=False):
        super().__init__(page_link, force_from_page=force_from_page)
        self.soup = self.get_soup()

    def get_soup(self):
        soup = BeautifulSoup(self.get_content(self.page_link), 'html.parser')
        # html_text = soup.prettify()
        return soup


class BaseLxml(Base):
    def __init__(self, page_link, force_from_page=False):
        super().__init__(page_link, force_from_page=force_from_page)
        self.tree = self.get_tree()

    def get_tree(self):
        tree = etree.HTML(self.get_content(self.page_link))
        return tree

