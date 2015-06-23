#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unidecode import unidecode 
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from datetime import datetime, date
import MySQLdb
import numpy as np
import json
import urllib2
import MySQLdb
import pandas as pd
from sqlalchemy import create_engine
import urllib, urllib2, cookielib
import csv
from dateutil.relativedelta import relativedelta
import numpy as np


def text_clean(text):
	text = text.replace('—','-')
	text = text.replace('–','-')
	text = text.replace('-','-')
	text = text.replace('）',')').replace('（','(')
	text = text.replace(' ','')
	text = text.replace('　','')
	text = text.replace('/','-')
	return text

name_dict = {}
for row in csv.reader(open('2015-06-15.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-13.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-13.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-12.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-11.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-10.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-09.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-08.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-07.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-06.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

name_dict = {}
for row in csv.reader(open('2015-06-05.csv','rb')):
	name_dict[text_clean(row[5])]=row[3]

w = open('code_name.txt','wr')
w.write('name,code\n')
#print name_dict
print len(name_dict)
for name in name_dict:
	w.write(name+','+name_dict[name]+'\n')
w.close()

def findName(code):
	tmp_dict = {}
	for row in csv.DictReader(open('code_name.txt','rb')):
		tmp_dict[row['code']] = row['name']
	return tmp_dict[code]

def updateName(name,code):
	name_dict = {}
	for row in csv.DictReader(open('code_name.txt','rb')):
		name_dict[row['code']] = row['name']
	name_dict[name] = code
	
	w = open('code_name.txt','wr')
	for name in name_dict:
		w.write(name+','+name_dict[name]+'\n')
	w.close()

#print findName('IE00B961PR15')


df_all = pd.read_csv('all-Taiwan-df.csv')
col = df_all.columns.tolist()
tmp_dict = {}
for name in col:
	tmp_dict[name] = text_clean(name)
df_all = df_all.rename(columns=tmp_dict)
df_all = df_all.rename(columns=name_dict)
df_all.to_csv('all-Taiwan-df.csv', index=False)
