#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 13:05:24 2021

@author: aptitude
"""

from flask import Flask, render_template, request, flash, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rxRoute', methods=['GET', 'POST'])
def rxRoute():
    if request.method == 'POST':
        drug = request.form['drug']
        print(drug)
        return render_template('rxFill.html', drug=drug)
    return render_template('rxFill.html')

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