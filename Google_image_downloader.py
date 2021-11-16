""" Download images from google using Selenium"""

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import time
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import random

if not os.path.exists("./images"):
    os.mkdir("./images")


def download_image(url, user_path, i):
    """Download image  url: image url
    user_path: images will be saved in this path
    i : just a counter """
    img_obj = requests.get(url)
    image = Image.open(BytesIO(img_obj.content))
    try:
        image.save(user_path + f"_{random.randint(1,9999)}_{random.randint(1,9999)}_{i}.{image.format}", image.format)
    except IOError:
        print("Can not save image")


def run_search():
    # wait for user to enter the required search phrase
    search = input("Search for: ")
    now = time.strftime('%d-%b-%Y-%H-%M-%S', time.localtime())
    if not os.path.exists(f"./images/{search}"):
        os.mkdir(f"./images/{search}")
    if not os.path.exists(f"./images/{search}/{search}-{now}"):
        os.mkdir(f"./images/{search}/{search}-{now}")
    # initiating the selenium
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    s = Service(executable_path="your_path\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    search_url = f"https://www.google.com/search?q={search}&source=lnms&tbm=isch"
    driver.get(search_url)

    # ask user to scroll the page
    user_command = "n"
    while user_command != "y":
        user_command = input("Scroll the page as much as you need then press y"
                             "\npress q to terminate the program : ").lower()
        if user_command == "q":
            exit()

    # Scrolling all the way up
    driver.execute_script("window.scrollTo(0, 0);")

    page_html = driver.page_source
    pagesoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pagesoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})

    print(f"{len(containers)} Images have been found")

    path = f"./images/{search}/{search}-{now}/{search}"

    SUCCESSFUL_DOWNLOADS = 0

    for i in range(1, len(containers)+1):
        # most of the times there are some links instead of images on positions number 25th,50th,75th...
        if i % 25 == 0:
            continue

        try:
            # Click on each Image Container
            driver.find_element(by=By.XPATH, value=f"""//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]""").click()
            time.sleep(2.5)
            # Grabbing the url
            image_preview_xpath = """//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img"""
            image_preview_element = driver.find_element(by=By.XPATH, value=image_preview_xpath)
            image_preview_url = image_preview_element.get_attribute("src")

            try:
                download_image(image_preview_url, path, i)
                print(f"image number {i} has been downloaded")
                SUCCESSFUL_DOWNLOADS += 1
            except:
                print(f"Couldn't download image number {i}, continuing downloading process")
        except:
            pass
    final_path = os.getcwd()+path.replace('/','\\')[1:path.rindex('/',)]
    print(f"downloading process has been completed, you can check the folder {final_path} \n{SUCCESSFUL_DOWNLOADS} "
          f"images have been downloaded successfully "
          f"\nunsuccessful downloads:  {len(containers) - SUCCESSFUL_DOWNLOADS}")

    user_continue_command = ""
    while user_continue_command != "y" and user_continue_command != "n":
        user_continue_command = input("Do you want search again(y/n)? ").lower()
    if user_continue_command == "n":
        exit()
    else:
        run_search()


run_search()

