# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pandas

file = pandas.read_csv("/Users/aptitude/Downloads/DrugXML.csv")

drugArray = []
for n in range(len(file)):
    drugArray.append(file.iloc[n, 0].replace("https://www.goodrx.com/",""))
    
file['drug'] = drugArray

drugs = pandas.DataFrame(drugArray)
drugs.to_csv("/Users/aptitude/Downloads/DrugNames.csv")


file.to_csv("/Users/aptitude/Downloads/DrugFull.csv")