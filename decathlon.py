from base import Base
import json
import re


class Decathlon(Base):

    NAME = 'decathlon'

    def __init__(self, page_link, from_file=True):
        super().__init__(page_link, from_file=from_file)
        self.content = self.get_content(page_link)
        self.json = self.get_json()

    def get_file_name(self):
        return self.page_link.split('#')[0].split('/')[-1]

    def get_json(self):
        regex_temp = re.compile(r"(?<=prestashop.page.product=)(.*});")
        regex_json = regex_temp.findall(self.content)
        return json.loads(regex_json[0])

    def get_brand_id(self):
        return self.json.get('brand')

    def get_store_id(self):
        return self.NAME

    def get_product_id(self):
        return self.json.get('id_super_model')

    def get_variants(self):
        pass

    def get_attributes(self):
        pass

    def get_assets(self):
        pass

    def get_breadcrumbs(self):
        pass

    def get_descr(self):
        pass

    def get_variantSelectors(self):
        pass
