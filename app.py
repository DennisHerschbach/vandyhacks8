#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 13:05:24 2021

@author: aptitude
"""

from flask import Flask, render_template, request, flash, url_for, redirect
from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
import pandas as pd
import os
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rxRoute', methods=['GET', 'POST'])
def rxRoute():
    if request.method == 'POST':
        global drug
        drug = request.form['drug']
        print(drug)
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        
        
            
            
        drug_url = "https://www.goodrx.com/" + drug
        driver.get(drug_url)
        sleep(5)
        
        soup = bs(driver.page_source, 'html.parser')
        
        def getBrandNames():
            brandclicker = driver.find_element_by_xpath("//*[@id='uat-dropdown-brand']").click()
            sleep(5)
            brandnames = driver.find_elements_by_class_name("option-3JfJd")
        
            if(len(brandnames) == 0):
                brandnames = soup.find_all('div', attrs = {"class":"label-3WJxw label_with_props_padding-1OqSo"}) 
        
            brandList = []
            for i in brandnames:
                brandList.append(i.text)
        
        
            return brandList
        
        
        def getFormNames():
            formclicker = driver.find_element_by_xpath("//*[@id='uat-dropdown-form']/span").click()
            sleep(5)
            formnames = driver.find_elements_by_class_name("option-3JfJd")
        
            if(len(formnames) == 0):
                formnames = soup.find_all('span', attrs = {"class":"labelText-1S74- labelText_form-2mDSe labelText-1S74-"}) 
                
            formList = []
            for i in formnames:
                formList.append(i.text)
            
            return formList
        
        
        def getDosageNames():
            dosageclicker = driver.find_element_by_xpath("//*[@id='uat-dropdown-dosage']/span").click()
            sleep(5)
            dosagenames = driver.find_elements_by_class_name("option-3JfJd")
        
            if(len(dosagenames) == 0):
                dosagenames = soup.find_all('span', attrs = {"class":"labelText-1S74- labelText_dosage-ChiO0"}) 
        
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
        
        brands = getBrandNames()
        forms = getFormNames()
        dosages = getDosageNames()
        quantitys = getQuantityNames()
        
        print(brands)
        print(forms)
        print(dosages)
        print(quantitys)
        
        return render_template('rxFill.html', drug=drug, brands=brands, forms=forms, dosages=dosages, quantitys = quantitys)
    return render_template('rxFill.html')

@app.route('/rxRouteOne', methods=['POST'])
def rxRouteOne():
    brandChoice = request.form['brandChoice']
    formChoice = request.form['formChoice']
    dosageChoice = request.form['dosageChoice']
    quantityChoice = request.form['quantityChoice']
    
    print(brandChoice)
    print(formChoice)
    print(dosageChoice)
    print(quantityChoice)
    
    def drugPermutations(drugName, brand, form, dosage, quantity):
    
        brand = brand[0:brand.index('(')-1]
        brand = brand.lower()
    
        quantity = quantity[0:quantity.index(' ')]
    
        form = form.lower()
        form = form.replace(' ', '-')
        
        specialchars = ' /'
        for specialchar in specialchars:
            dosage = dosage.replace(specialchar,'-')
    
        url = 'https://www.goodrx.com/' + drugName + '?dosage=' + dosage + '&form=' + form + '&label_override=' + brand + '&quantity=' + quantity + '&sort_type=popularity'
        return url
    
    print(drug)
    choiceUrl = drugPermutations(drug, brandChoice, formChoice, dosageChoice, quantityChoice)
    
    def scraper(drug_url):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
        
        driver.get(drug_url)
        sleep(5)
        soup = bs(driver.page_source, 'html.parser')
    
        allprices = soup.find_all('div', attrs={"data-qa":"drug_price"})
    
        
    
        
        storenames = soup.find_all('span', attrs={"class":"goldAddUnderline-3T_sh"})
        
        if(len(allprices) == 0):
            return("We could not find the drug you were looking for.\n\nThis could be due to any one of the following reasons:\n1) The drug is not commercially available\n2) The drug is not approved by the FDA\n3) It is a limited distribution drug and not available at pharmacies\n4) You need a prescription for it and your healthcare provider must give you one")
        else:
            dict  = {'Store name': 'prices'}
            for i in range(0,len(allprices)):
                dict[storenames[i].text] = allprices[i].text.replace('The  price after coupon is', '').replace('The retail price  is', '')
                
        for i in dict.keys():
            dict[i] = dict[i][0:len(dict[i]) - 1]
    
        companyList = ['Kroger Pharmacy', 'Walgreens', 'CVS Pharmacy', 'Publix', 'Walmart', 'Costco', 'Food City Pharmacy', 'Target (CVS)', 'Walmart Neighborhood Market']
        ctr = 0
        prices = []
        for i in companyList:
            if(i in dict):
                prices.append(dict.get(i))
            else:
                prices.append(None)
    
        driver.quit()
        return prices
        
    result = scraper(choiceUrl)
    
    print(result)
    
    for n in range(1, 10):
        if (result[n-1] == result[n-1]):
            if n == 1:
                kroger = True
            elif n == 2:
                walgreens = True
            elif n == 3:
                cvs = True
            elif n == 4:
                publix = True
            elif n == 5:
                walmart = True
            elif n == 6:
                costco = True
            elif n == 7:
                foodcity = True
            elif n == 8:
                target = True
            elif n == 9:
                walmartneighborhood = True
            
    
    return render_template('rxFill.html', result=result, kroger=kroger, walgreens=walgreens, cvs=cvs, publix=publix, walmart=walmart, costco=costco, foodcity=foodcity, target=target, walmartneighborhood=walmartneighborhood)

@app.route('/medRoute', methods=['GET', 'POST'])
def medRoute():
    if request.method == 'POST':
        treatment = request.form['treatment']
        print(treatment)
        
        import pandas as pandas

        file = pandas.read_csv("ClinicData.csv", encoding = "ISO-8859-1")

        treatmentArray = []
        for n in range(len(file)):
            treatmentArray.append(file.iloc[n, 0])

        treatmentDF = file.loc[file['Illnesses'] == treatment]

        index = treatmentDF.index.values[0]

        priceList = []
        
        cvs = ""
        kroger = ""
        walmart = ""
        costco = ""
        walgreens = ""
        for n in range(1, 6):
            if (file.iloc[index, n] == file.iloc[index, n]):
                priceList.append(file.iloc[index, n])
                if n == 1:
                    cvs = True
                elif n == 2:
                    kroger = True
                elif n == 3:
                    walmart = True
                elif n == 4:
                    costco = True
                elif n == 5:
                    walgreens = True
                
        
        return render_template('medFill.html', treatment=treatment, priceList=priceList, cvs=cvs, kroger=kroger, walmart=walmart, costco=costco, walgreens=walgreens)
    return render_template('medFIll.html')

if __name__=='__main__':
    app.run(debug=True)