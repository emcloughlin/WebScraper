from typing import ItemsView
from pandas.core.frame import DataFrame
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Read and store the list of search terms
keywords = pd.read_csv('searchTerms.csv')
serverURI = input("Enter the Selenium Server Address: ")


def search_web(query, iteration):
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={query}"

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--allow-cross-origin-auth-prompt')

    driver = webdriver.Remote(
        command_executor=serverURI,
        options=options
    )

    # Search the web for the given query
    driver.get(search_url)

    # XPath for the first image in a google search
    img_box = driver.find_element_by_xpath(f'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[{iteration}]/a[1]/div[1]/img')
    # Click on the image thumbnail
    time.sleep(random.randint(1, 2))
    img_box.click()

    # XPath for the image display box
    display_box = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')
    # Click on the display
    time.sleep(random.randint(1, 2))
    display_box.click()

    image_src = display_box.get_attribute('src')

    driver.quit()

    return image_src


# Creating header for file containing image source link
with open("imageLinks.csv", "w") as outfile:
    outfile.write("search_terms|src_link\n")

# Loops through the list of search input
pastaDict = ['Penne', 'Spaghetti', 'Macaroni', 'Tortellini']
pastaCount = 0
dictCount = 0
for keyword in keywords['pasta']:
    pastaCount = 0
    for x in range(1, 1000):
        try:
            link = search_web(keyword, x)
            keyword = keyword.replace(" ", "_")
            with open("imageLinks.csv", "a") as outfile:
                outfile.write(f"{keyword}|{link}\n")
            pastaCount += 1
            print("Current Pasta: " pastaDict[dictCount] + "Links collected")
        except Exception as e:
            print(e)
    dictCount += 1
