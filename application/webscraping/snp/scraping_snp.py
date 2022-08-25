import requests
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime


def download_pdf(url):
    """

    :param url: The S&P page you want to download a pdf from.
    :type url: string

    :return: pdf download
    :rtype: file

    """
    # download_file(url='https://www.spglobal.com/ratings/en/research/pdf-articles/220818-presale-japan-housing-finance-agency-series-184-12474649')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name, 'snp_pdfs')
    if not os.path.exists(path):
        os.makedirs(path)

    endpoint = url.split('/')[-1]
    file_date = endpoint.split('-')[0]
    file_name = os.path.join(dir_name, 'snp_pdfs', endpoint + '.pdf')

    if file_date.isdigit():
        # We only want reports from the last 31 days, so we need to compare their
        # publication date to current date
        now = datetime.now()
        pub_date = datetime.strptime(str(file_date), '%y%m%d')
        pub_age = now - pub_date

        if pub_age.days <= 31:
            for link in links:
                item = link.get('href', [])
                if '.pdf' in link.get('href', []):
                    response = requests.get('https://www.spglobal.com' + item)
                    pdf = open(file_name, 'wb')
                    pdf.write(response.content)
                    pdf.close()
                    return 1
        else:
            return 0
    else:
        return 0


# https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex
def multiple_replace(dictionary, text):
    """

        :param dictionary: The dictionary that defines replacements
        :type dictionary: dict

        :param text: The text on which you want to execute the replacements
        :type text: string

        :return: formatted link to S&P research for that industry
        :rtype: string

        """
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dictionary.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dictionary[mo.string[mo.start():mo.end()]], text)


def update_provider_url(industry):
    """

    :param industry: The industry for which you want to find file for
    :type industry: string

    :return: formatted link to S&P research for that industry
    :rtype: string

    """
    # Industry with some regex to make it valid for a url.
    # for example 'Infrastructure & Utilities' becomes 'Infrastructure%20%26%20Utilities'
    replacement_dict = {
        ' ': '%20',
        '&': '%26',
        '"': '%22'
    }
    updated_industry = multiple_replace(replacement_dict, industry)

    # The provider of the files
    target = 'https://www.spglobal.com/ratings/en/research-insights/researchfullfeed.aspx?q' \
             f'=custom_ss_theme_full:(%220/{updated_industry}%22)'.format(updated_industry=updated_industry)

    return target


def get_documents(industry):
    """

    :param industry: The industry for which you want to download files for from S&P.
    :type industry: string

    :return: multiple pdf download
    :rtype: multiple files

    """
    target = update_provider_url(industry)
    response = requests.get(target)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    files_downloaded = 0
    for link in links:
        item = link.get('href', [])
        if (
                isinstance(item, str)
                and len(item.split('/')) > 3
                and item.split('/')[3] == 'research'
                and item.split('/')[4] == 'pdf-articles'
                and not item.split('/')[5].__contains__('presale')
        ):
            files_downloaded = files_downloaded + download_pdf('https://www.spglobal.com' + item)

    return files_downloaded
