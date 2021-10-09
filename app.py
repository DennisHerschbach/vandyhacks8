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
        return 

    # show the form, it wasn't submitted
    return render_template('med.html')