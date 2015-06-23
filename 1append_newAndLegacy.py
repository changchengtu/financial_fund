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

##############  daily data download  ##############


today = datetime.today().date()
LaDate = str(today)


# file coding: utf-16le with dom

## conver int to string
def date_str(o_str):
	o_str = str(o_str)
	return o_str[0:4]+'-'+o_str[4:6]+'-'+o_str[6:]

def text_clean(text):
	text = text.replace('—','-')
	text = text.replace('）',')').replace('（','(')
	text = text.replace(' ','')
	text = text.replace('/','-')
	return text

## get data
def get_t_data_today(LaDate):
	fund_url = 'https://members.sitca.org.tw/OPF/K0000/files/F/03/nav.csv'

	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	resp = opener.open(fund_url)
	ori =  resp.read().decode('utf-16le').encode('utf-8')

	## save file
	open('Taiwan/new_funds_data/'+LaDate+'.csv', 'wr').write(ori)

	df = pd.read_csv('Taiwan/new_funds_data/'+LaDate+'.csv')
	return df


## append data
def append_newAndLegacy(name):
	df_legacy = pd.read_csv('Taiwan/all-Taiwan.csv')
	df_new = pd.read_csv('Taiwan/new_funds_data/'+name+'.csv')

	## convert date
	cols = df_new.columns.tolist()
	df_new['日期'] = df_new[cols[0]]
	df_new['日期'] = df_new.apply(lambda row : date_str(row['日期']), axis = 1)
	df_new = df_new.drop(cols[0], 1)
	
	## append
	df_all = df_new.append(df_legacy)

	## drop useless columns
	df_all = df_all.drop_duplicates(subset=['基金名稱','日期'])
	df_all = df_all.drop('基金代號', 1)
	df_all = df_all.drop('漲跌幅', 1)


	return df_all


## get data today
get_t_data_today(LaDate)

## append to legacy data
df_all = append_newAndLegacy(LaDate)
df_all.to_csv('Taiwan/all-Taiwan.csv', index=False)


## process data into better format
df_all = pd.read_csv('Taiwan/all-Taiwan.csv')


## tmp variables
tmp_df = None
first = True

for df in df_all.groupby('基金名稱'):
	name_fund = df[0]
	#print name_fund 
	df_fund = df[1][['日期','基金淨值']].rename(columns={'基金淨值':name_fund})

	if first == True:
		tmp_df = pd.DataFrame(df_fund)
		first = False
	else:
		tmp_df = tmp_df.merge(df_fund, how='outer', on=['日期'])

## ordering 
tmp_df = tmp_df.sort(['日期'], ascending=[1])

tmp_df.to_csv('Taiwan/all-Taiwan-df.csv', index=False)

print 'Taiwan is finished'


######## foreign folder
## get data
def get_f_data_today(LaDate):
	fund_url = 'http://smart.tdcc.com.tw/opendata/getOD.ashx?id=3-4'

	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	resp = opener.open(fund_url)
	ori = text_clean(resp.read())

	## save file
	open('Foreign/new_funds_data/'+LaDate+'_foreign.csv', 'wr').write(ori)

	df = pd.read_csv('Foreign/new_funds_data/'+LaDate+'_foreign.csv')
	return df

all_df = pd.read_csv('Foreign/all-Foreign-df.csv')
old_cols = all_df.columns.tolist()
new_cols = []
for name in get_f_data_today(LaDate)['基金名稱']:
	new_cols.append(name)


## build a new dataframe
new_all_dict = {}
new_all_cols = list(set(new_cols+old_cols)) ## remove duplicated names

date_arr = []
tmp_arr = []
weekend = set([5, 6])
for d in range((datetime.now()-(datetime.now() - relativedelta(years=3))).days):
	a_date = today-relativedelta(days=d)
	if a_date.weekday() not in weekend:
		tmp_arr.append(np.nan)
		date_arr.append(str(a_date))

new_all_dict['日期']=date_arr
#new_all_dict['日期']=[]
for name in new_all_cols:
	if name == '日期':
		None
		#new_all_dict[name] = date_arr
		#new_all_dict[name] = []
	else:
		new_all_dict[name] = tmp_arr

new_all_df = pd.DataFrame(new_all_dict)
##for insert
new_all_df.index = new_all_df['日期']
#print new_all_df



## insert old data
for index, row in all_df.iterrows():
	row = row.to_dict()
	date=row['日期']
	row.pop('日期')

	for key, value in row.iteritems():
		## 3 years only
		if date in date_arr:
			new_all_df.loc[date, key] = value

#print new_all_df
## format new data into proper dataframe
new_df = get_f_data_today(LaDate)

## insert new data
for index, row in new_df.iterrows():
	row = row.to_dict()
	date=row['日期']
	name = row['基金名稱']
	value = row['基金淨值']
	## 3 years only
	if date in date_arr:
		new_all_df[name][date]=value


#print new_all_df
	

#new_all_df = new_all_df.drop_duplicates(['日期'])
new_all_df = new_all_df.sort(['日期'], ascending=[1])

new_all_df.to_csv('Foreign/all-Foreign-df.csv',index=False)
print 'Foreign os finished'

