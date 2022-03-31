import os
import sys

sys.path.append("../")
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from setproctitle import setproctitle
from datetime import datetime, date, timedelta, timezone
import pandas as pd
import numpy as np
import re
import urllib.parse



def starting_driver(urlpage, chrome_options):
    driver = webdriver.Chrome(executable_path=CONFIG.get_chrome_driver_path(),
                              chrome_options=chrome_options)
    LOGGER.info(urlpage)
    driver.get(urlpage)
    LOGGER.info("Successfully started the selenium driver")
    return driver


def testing_driver(chrome_options):
    driver = webdriver.Chrome(executable_path=CONFIG.get_chrome_driver_path(),
                              options=chrome_options)
    driver.get("http://google.com")
    if driver.title == "Google":
        driver.close()
        LOGGER.info("Selenium Driver is working fine")
    else:
        driver.close()
        raise Exception(
            "Selenium Driver not able to download any test webpage")


def reading_all_urls(driver):
    urls = []
    try:
        myElem = WebDriverWait(driver,
                               int(CONFIG.get_chrome_driver_delay())).until(
                                   EC.presence_of_element_located(
                                       (By.CLASS_NAME, "ResultLink")))
        out = driver.find_elements_by_class_name("ResultLink")
        for j in out:
            url_attribute = j.get_attribute("href")
            if url_attribute.startswith(
                    "https://sample/"
            ) and not url_attribute.endswith("#tab-history"):
                urls.append(url_attribute)
        urls = set(urls)
        LOGGER.info("Successfully read all the urls")
    except:
        LOGGER.info("No data available for the given dates.")
    return urls


def reading_text(driver):
    scope_text = (WebDriverWait(driver,
                                int(CONFIG.get_chrome_driver_delay())).until(
                                    EC.presence_of_element_located(
                                        (By.CLASS_NAME, "scope"))).text)
    scope_text = scope_text.replace("SCOPE\n", "")
    
    LOGGER.debug("Success")
    return scope_text



def epoch_to_percent_encode(value):
    readable_value = datetime.utcfromtimestamp(value / 1000)
    reformatted_value = datetime.strftime(readable_value, '%Y/%m/%d@%H:%M:%S')
    reformatted_value = urllib.parse.quote(reformatted_value, safe='')
    return reformatted_value


def main():
  
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server=%s" %
                                    CONFIG.get_http_proxy())
        chrome_options.add_argument("--proxy-server=%s" %
                                    CONFIG.get_https_proxy())
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1420,1080")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
       
        testing_driver(chrome_options)
        driver = starting_driver(urlpage, chrome_options)
        urls = reading_all_urls(driver)
        driver.close()
     

        for url in urls:

            driver = starting_driver(url, chrome_options)
            data = reading_data(driver)
            


if __name__ == "__main__":
    main()
