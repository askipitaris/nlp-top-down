import requests
import zope.interface
from bs4 import BeautifulSoup
from pathlib import Path
from scraping_interface import ScrapingInterface


@zope.interface.implementer(ScrapingInterface)
class ScrapingSNP:
    def download_file(self, url):
        pass

    def update_provider_url(self, industry):
        # Industry with some regex to make it valid for a url.
        # ' ' becomes %20
        # '&' becomes %26
        # '"' becomes %22
        # for example 'Infrastructure & Utilities' becomes 'Infrastructure%20%26%20Utilities'
        industry_replaced_char = ''

        # The provider of the files
        provider = 'https://www.spglobal.com/ratings/en/research-insights/researchfullfeed.aspx?q' \
                   f'=custom_ss_theme_full:(%220/{industry_replaced_char}%22)'\
            .format(industry_replaced_char=industry_replaced_char)

        return provider

    def get_documents(self, industry):
        pass
