import os
import time
from string import Template

import requests
from bs4 import BeautifulSoup
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
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('.button__download')
    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name, 'snp_pdfs')
    if not os.path.exists(path):
        os.makedirs(path)

    endpoint = url.split('/')[-1]
    file_name = os.path.join(dir_name, 'snp_pdfs', endpoint + '.pdf')

    for link in links:
        item = link.get('href', [])
        if '.pdf' in item:
            response = requests.get('https://www.spglobal.com' + item)
            pdf = open(file_name, 'wb')
            pdf.write(response.content)
            pdf.close()
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
    files_downloaded = 0
    driver = get_page_contents(industry)
    elements = driver.find_elements(By.XPATH, "//a[@class='modalimage card--inline js-gtm-tag gtm-bound']")

    for element in elements:
        item = element.get_attribute('href')
        if '/pdf-articles/' in item:
            # files_downloaded = files_downloaded + download_pdf(article)
            print("pdf!", item)
            files_downloaded = files_downloaded + download_pdf(item)
        elif '/articles' in item:
            print("article!", item)

    driver.close()
    return files_downloaded
