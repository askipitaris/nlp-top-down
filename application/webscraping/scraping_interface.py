import zope.interface

"""

An interface for web scrapers. Each implementation of webscraper will have a unique structure based off the targer 
you are scraping from

"""


class ScrapingInterface(zope.interface.Interface):
    def download_file(self, url):
        """

        :param url: The page you want to download a pdf of.
        :type url: string

        :return: pdf download
        :rtype: file

        """
        pass

    def update_provider_url(self, industry):
        """

        :param industry: The industry you want to embed into the provider url. Spaces should be replaced with %20
        and & should be replaced with %26. Double quotes are %22
        :type industry: string

        :return: url
        :rtype: string

        """
        pass

    def get_documents(self, industry):
        """

        :param industry: The industry for which you want to which to download all documents from this provider
        :type industry: string

        :return: multiple pdf download
        :rtype: multiple files

        """
        pass
