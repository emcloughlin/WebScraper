from selenium import webdriver
import pandas as pd
import time
import random


# Read and store the list of search terms
keywords = pd.read_csv('searchTerms.csv')
serverURI = input("Enter the Selenium Server Address: ")


def init_driver():
    """ Initialze the remote webdriver with the specified options. """
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

    return driver


def close_driver(driver):
    """ Shutdown the webdriver. """
    driver.quit()


def search_web(driver, query):
    """
    Search the web for the provided search term.

    Args:
    query -- the term to be searched
    """
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={query}"

    # Search the web for the given query
    driver.get(search_url)


def get_Nth_image_src(driver, image_count):
    """
    Returns the src attribute of the specified image

    Args:
    image_count -- the selected image to return the attributes of
    """
    # XPath for the first image in a google search
    img_box = driver.find_element_by_xpath(f'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[{image_count}]/a[1]/div[1]/img')
    # Click on the image thumbnail
    time.sleep(random.randint(1, 2))
    img_box.click()

    # XPath for the image display box
    display_box = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')
    # Click on the display
    time.sleep(random.randint(1, 2))
    display_box.click()

    image_src = display_box.get_attribute('src')

    return image_src


driver = init_driver()

# Creating header for file containing image source link
with open("imageLinks.csv", "w") as outfile:
    outfile.write("search_terms|src_link\n")

# Loops through the list of search input
pastaDict = ['Spaghetti', 'boiled spaghetti', 'plain spaghetti',
             'spaghetti pasta', 'cooked spaghetti', 'macaroni',
             'boiled macaroni', 'plain macaroni', 'macaroni pasta',
             'cooked macaroni', 'tortellini', 'boiled tortellini',
             'plain tortellini', 'tortellini pasta', 'cooked tortellini']
pastaCount = 0
dictCount = 0
for keyword in keywords['pasta']:
    pastaCount = 0
    search_web(driver, keyword)
    for x in range(1, 100):
        try:
            link = get_Nth_image_src(driver, x)
            keyword = keyword.replace(" ", "_")
            with open("imageLinks.csv", "a") as outfile:
                outfile.write(f"{keyword}|{link}\n")
            pastaCount += 1
            print("Current Pasta: " + pastaDict[dictCount] + ", Links " +
                  "collected = {linkNum}".format(linkNum=pastaCount))
        except Exception as e:
            print(e)
    dictCount += 1

close_driver(driver)
