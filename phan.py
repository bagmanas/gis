__author__ = 'Bagman'
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os



# Mega driver
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : os.path.abspath("./data_from_gks")}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path= os.path.abspath("./chromedriver.exe"), chrome_options=chromeOptions)
driver.set_window_size(1120, 550)


for id in range(99):
    page = "http://www.gks.ru/dbscripts/munst/munst{}/DBInet.cgi".format(id)
    if requests.get(page).status_code == 404:
        continue
    driver.get(page)
    v = driver.find_elements_by_class_name('subhead')
    s = set()
    s.add('g0')
    for el in v:
        print(el.get_attribute('id'))
        if el.is_displayed() and el.get_attribute('id') not in s:
            el.click()
            s.add(el.get_attribute('id'))

    driver.find_element_by_name('p8112027').click()
    driver.find_element_by_id('Knopka').click()

    for el in driver.find_elements_by_xpath("//input[@type='checkbox']"):
        if not el.is_selected():
            el.click()
    el = driver.find_element_by_name('STbl').click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])

    el = driver.find_element_by_name('Format')
    driver.save_screenshot('screen2.png')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'CSV':
            option.click()
            break

    driver.find_element_by_xpath("//input[@type='button']").click()












