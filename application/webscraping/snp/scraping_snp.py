import os
import time
import codecs
from string import Template

import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def download_pdf(url):
    """

    :param url: The S&P page you want to download a pdf from.
    :type url: string

    :return: pdf download
    :rtype: file

    """
    response = requests.get(url)
    tree = html.fromstring(response.text)
    download_link = tree.xpath("//a[@class='button--red button__download']/@href")[0]

    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name, 'snp_files')
    if not os.path.exists(path):
        os.makedirs(path)

    endpoint = url.split('/')[-1]
    file_name = os.path.join(dir_name, 'snp_files', endpoint + '.pdf')

    if '.pdf' in download_link:
        response = requests.get('https://www.spglobal.com' + download_link)
        pdf = open(file_name, 'wb')
        pdf.write(response.content)
        pdf.close()
        return 1
    return 0


def download_text(url):
    """

    :param url: The S&P page you want to download a text file from.
    :type url: string

    :return: text file download
    :rtype: file

    """
    response = requests.get(url)
    tree = html.fromstring(response.text)
    text = tree.xpath("//div[@id='researchContent']//text()")

    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name, 'snp_files')
    if not os.path.exists(path):
        os.makedirs(path)

    endpoint = url.split('/')[-1]
    file_name = os.path.join(dir_name, 'snp_files', endpoint + '.txt')

    text_file = codecs.open(file_name, 'w', 'utf-8')
    for line in text:
        text_file.write(line)
    text_file.close()

    return 1


def get_page_contents(industry):
    """

    :param industry: The S&P page you want to download a pdf from.
    :type industry: string

    :return: driver
    :rtype: webdriver with filter's applied

    """
    xpath = Template("//label[@for='$industry']")

    firefox_options = Options()
    # firefox_options.add_argument("--headless")

    # Downloads drivers to C:\Users\<User>\.wdm\drivers on windows or user.home/.wdm
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
    driver.get('https://www.spglobal.com/ratings/en/research-insights/researchfullfeed.aspx')
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath.substitute({'industry': industry}))))

    driver.find_element(By.XPATH, xpath.substitute({'industry': industry})).click()
    time.sleep(1)

    return driver


def get_documents(industry):
    """

    :param industry: The industry for which you want to download files for from S&P.
    :type industry: string.

    :return: multiple pdf download
    :rtype: multiple files

    """
    pdfs_downloaded = 0
    text_files_downloaded = 0
    driver = get_page_contents(industry)
    elements = driver.find_elements(By.XPATH, "//a[@class='modalimage card--inline js-gtm-tag gtm-bound']")

    for element in elements:
        item = element.get_attribute('href')
        if '/pdf-articles/' in item:
            pdfs_downloaded = pdfs_downloaded + download_pdf(item)
        elif '/articles' in item:
            text_files_downloaded = text_files_downloaded + download_text(item)

    driver.close()
    return {'pdfs': pdfs_downloaded, 'text_files': text_files_downloaded}
