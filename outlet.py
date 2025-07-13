#from bs4 import BeautifulSoup
# import requests
# import json
# import re
from base import BaseSoup


class Outlet(BaseSoup):

    NAME = 'outlet'

    def get_brand_id(self):
        return 'outlet'

    def get_store_id(self):
        return 'outlet'

    def get_breadcrumbs(self):
        path = self.soup.find_all('div', class_='product-breadcrumb')
        print(path)

    def get_price(self):
        path = self.soup.find_all('script', type='application/ld+json')[0]
        print(path)