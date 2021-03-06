from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
import pandas as pd
import os
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)




drug_url = "https://www.goodrx.com/" + "zoloft"
driver.get(drug_url)
sleep(5)

soup = bs(driver.page_source, 'html.parser')

def getBrandNames():
    brandclicker = driver.find_element_by_xpath("//*[@id='uat-dropdown-brand']").click()
    sleep(5)
    brandnames = driver.find_elements_by_class_name("option-3JfJd")

    brandList = []
    for i in brandnames:
        brandList.append(i.text)


    return brandList


def getFormNames():
    formclicker = driver.find_element_by_xpath("//*[@id='uat-dropdown-form']/span").click()
    sleep(5)
    formnames = driver.find_elements_by_class_name("option-3JfJd")
         
         
    formList = []
    for i in formnames:
        formList.append(i.text)
    
    return formList


def getDosageNames():
    dosageclicker = driver.find_element_by_xpath("//*[@id='uat-dropdown-dosage']/span").click()
    sleep(5)
    dosagenames = driver.find_elements_by_class_name("option-3JfJd")

    dosageList = []

    for i in dosagenames:
        dosageList.append(i.text)

    return dosageList


def getQuantityNames():
    quantityclicker = driver.find_element_by_xpath("//*[@id='uat-dropdown-quantity']/span").click()
    sleep(5)
    quantitynames = driver.find_elements_by_class_name("option-3JfJd")

    quantityList = []
    for i in quantitynames:
        quantityList.append(i.text)

    return quantityList


print(getBrandNames())

print(getFormNames())

print(getDosageNames())

print(getQuantityNames())



