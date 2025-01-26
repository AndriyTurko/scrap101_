from bs4 import BeautifulSoup
from lxml import etree
import requests


class Base:

    NAME = ''

    def __init__(self, page_link, from_file=True):
        self.from_file = from_file
        self.page_link = page_link

    def get_file_name(self):
        raise NotImplementedError()

    def get_content(self, page_url, file_extention='txt'):
        file_path = 'temp_files/{}/{}.{}'.format(self.NAME, self.get_file_name(), file_extention)
        if self.from_file:
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
        variantSelectors = self.get_variantSelectors()
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
            'variantSelectors': variantSelectors,
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

    def get_variantSelectors(self):
        raise NotImplementedError()


class BaseSoup(Base):
    def __init__(self, page_link, from_file=True):
        super().__init__(page_link, from_file=from_file)
        self.soup = self.get_soup()

    def get_soup(self):
        soup = BeautifulSoup(self.get_content(self.page_link), 'html.parser')
        # html_text = soup.prettify()
        return soup


class BaseLxml(Base):
    def __init__(self, page_link, from_file=True):
        super().__init__(page_link, from_file=from_file)
        self.tree = self.get_tree()

    def get_tree(self):
        tree = etree.HTML(self.get_content(self.page_link))
        return tree

