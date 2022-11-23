from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    WebDriverException
# from selenium.webdriver.chrome.service import Service
# from chromedriver_py import binary_path  # this will get you the path variable
from webdriver_manager.chrome import ChromeDriverManager


def ShowMore_clicker(driver, t_seconds=2 ** 2):
    start_clicking_time = time.time()
    i = 0
    while True:
        i = i + 1
        try:
            start_loading_time = time.time()
            button = driver.find_element(By.CLASS_NAME, 'StateResults_button__DIGoI')
            driver.execute_script("arguments[0].click();", button)
            WebDriverWait(driver, t_seconds, 0.001).until(EC.element_to_be_clickable((By.CLASS_NAME, 'StateResults_button__DIGoI')))
            loading_time = time.time() - start_loading_time
            print(i, ", loading succeeded", ", using %s seconds" % loading_time)
        # NoSuchElementException - happens when the page does not have the button at all
        # TimeoutException - happens when the page is not fully loaded or no more buttons
        # ElementClickInterceptedException or WebDriverException
        except (NoSuchElementException) as e1:
            loading_time = time.time() - start_loading_time
            print(i, ", no such button", ", using %s seconds," % loading_time, repr(e1))
            break
        except (TimeoutException) as e2:
            loading_time = time.time() - start_loading_time
            print(i, ", loading failed", ", using %s seconds," % loading_time, repr(e2))
            break
        except (ElementClickInterceptedException, WebDriverException) as e3:
            loading_time = time.time() - start_loading_time
            print(i, ", need investigation", ", using %s seconds," % loading_time, repr(e3))
            break
    time_in_total = time.time() - start_clicking_time
    print("--- %s seconds in total ---" % time_in_total)
    return driver


class MyWebScraper(object):
    def __init__(self, url):
        self.search_link = url
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.search_link)

        init_page_source = BeautifulSoup(driver.page_source, 'lxml')
        num_benchmark = self.num_obs(init_page_source)
        # setting below is based on empirical evidence,
        # which is highly dependent on your working environment
        if int(num_benchmark) <= 400:
            t_seconds = 2 ** 2
        elif (int(num_benchmark) > 400) and (int(num_benchmark) <= 800):
            t_seconds = 2 ** 3
        else:
            t_seconds = 2 ** 5

        driver = ShowMore_clicker(driver, t_seconds)
        self.page_source = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()
        # time.sleep(500000)
        self.num_demand = self.num_obs(self.page_source)
        self.fundraisers_links = self.fundraiser_hunting()
        self.num_supply = len(self.fundraisers_links)

    def num_obs(self, x):
        try:
            num_obs_should_have = x.find('div', class_="heading-3").text.split(' results')[0]
            return int(num_obs_should_have)
        except:
            return 1000  # or "did not show up"; 1k is the maximum by website design

    def fundraiser_hunting(self):
        fundraisers_links_list = [x.get('href') for x in self.page_source.find_all('a')
                                  if "/f/" in x.get('href')]
        fundraisers_links_list = list(set(fundraisers_links_list))
        return fundraisers_links_list


# gofundmeObj = MyWebScraper('https://www.gofundme.com/s?q=&c=11')
# print('Result')
# print(gofundmeObj.fundraisers_links);