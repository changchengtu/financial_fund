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
for row in csv.reader(open('2015-06-13_foreign.csv','rb')):
	name_dict[text_clean(row[1])]=row[0]

name_dict = {}
for row in csv.reader(open('2015-06-16_foreign.csv','rb')):
	name_dict[text_clean(row[1])]=row[0]

name_dict = {}
for row in csv.reader(open('2015-06-22_foreign.csv','rb')):
	name_dict[text_clean(row[1])]=row[0]

name_dict = {}
for row in csv.reader(open('2015-06-19_foreign.csv','rb')):
	name_dict[text_clean(row[1])]=row[0]

w = open('code_name.txt','wr')
w.write('name,code\n')
#print name_dict
#print len(name_dict)
for name in name_dict:
	w.write(name+','+name_dict[name]+'\n')
w.close()

def findName(code):
	tmp_dict = {}
	for row in csv.DictReader(open('code_name.txt','rb')):
		tmp_dict[row['code']] = row['name']
	return tmp_dict[code]
print findName('IE00B961PR15')


df_all = pd.read_csv('all-Foreign-df.csv')
col = df_all.columns.tolist()
tmp_dict = {}
for name in col:
	tmp_dict[name] = text_clean(name)
df_all = df_all.rename(columns=tmp_dict)
df_all = df_all.rename(columns=name_dict)
df_all.to_csv('all-Foreign-df.csv', index=False)
