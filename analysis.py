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
pd.options.mode.chained_assignment = None 
from sqlalchemy import create_engine
from dateutil.relativedelta import relativedelta
import urllib, urllib2, cookielib
import csv
import ffTech as f
import shutil
import os
import inspect
import operator



today = datetime.today().date()
LaDate = str(today)

'''
## remove legacy folders
current_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
for path, subdirs, files in os.walk(current_folder+'/Taiwan/output'):
	for folder_name in subdirs:
		shutil.rmtree(current_folder+'/Taiwan/output/'+folder_name)
		os.mkdir(current_folder+'/Taiwan/output/'+folder_name)
'''

## remove legacy folders
current_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
for path, subdirs, files in os.walk(current_folder+'/Foreign/output'):
	for folder_name in subdirs:
		shutil.rmtree(current_folder+'/Foreign/output/'+folder_name)
		os.mkdir(current_folder+'/Foreign/output/'+folder_name)



def BIAS_ratio(name_list, df, threshold, check_long_goup=True):
	bias_dict = {}
	for name in name_list:
		try:
			ma_dict, df_period, df_short = f.MA(name,df)
		except:
			continue
		#long_goup_state = True
		#if check_long_goup:
			#long_goup_state = ma_dict['lon_going_up']
		
		## seasonal BIAS
		#if ma_dict['lon_s']>slope_rate and long_goup_state:
		if ma_dict['pre_bias_v'] < threshold:
			bias_dict[name] = ma_dict['pre_bias_v']

	return bias_dict


def top_N_bias(bias_dict, df, save_path, N):
	## top N bias
	sorted_bias_dict = dict(sorted(bias_dict.items(), key=operator.itemgetter(1), reverse=False)[:N])
	for fund_name in sorted_bias_dict:
		print fund_name
		ma_dict, df_period, df_short = f.MA(fund_name,df)
		rate = sorted_bias_dict[fund_name]
		f.plot_line(fund_name,str(rate)+'_'+fund_name, df_period, df_short, save_path)


print '\n-------------Foreign-------------'

## get data from csv
three_year = f.getForeignData(36, ['美元','USD','日期'])
six_m = f.getForeignData(6, ['美元','USD','日期'])
three_m = f.getForeignData(3, ['美元','USD','日期'])

nameF_list = six_m.columns.tolist()
nameF_list.remove('日期')

## classify funds
cat_df = pd.read_csv('fundF_category.csv')

stockF_list = []
bondF_list = [] 
indexF_list = []
balanceF_list = []
otherF_list = []
currencyF_list = []

#to get attribute name
attr = cat_df.columns.tolist()
fund_class = attr[3]
fund_name = attr[1]

# start comparing
for index, row in cat_df.iterrows():
	try:
		if '股票型' in row[fund_class]:
			stockF_list.append(f.text_clean(row[fund_name]))
		elif '固定收益型' in row[fund_class]:
			bondF_list.append(f.text_clean(row[fund_name]))
		elif '指數' in row[fund_class]:
			indexF_list.append(f.text_clean(row[fund_name]))
		elif '貨幣市場型' in row[fund_class]:
			currencyF_list.append(f.text_clean(row[fund_name]))
		elif '平衡型' in row[fund_class]:
			balanceF_list.append(f.text_clean(row[fund_name]))
		else:
			otherF_list.append(f.text_clean(row[fund_name]))
	except:
		print attr[2], attr[0], row[attr[2]], row[attr[0]]



print '--index--'
biasF_rate_dict = BIAS_ratio(indexF_list, three_year, 20)
top_N_bias(biasF_rate_dict, three_year, 'Foreign/output/index', 60)

print '--stock--'
biasF_rate_dict = BIAS_ratio(stockF_list, three_year, -4)
top_N_bias(biasF_rate_dict, three_year, 'Foreign/output/stock', 60)

print '--balance--'
biasF_rate_dict = BIAS_ratio(balanceF_list, three_year, 0)
top_N_bias(biasF_rate_dict, three_year, 'Foreign/output/balance', 60)

#print '--bond--'
#biasF_rate_dict = BIAS_ratio(bondF_list, three_year, 0)
#top_N_bias(biasF_rate_dict, three_year, 'Foreign/output/bond', 60)


print '-------------targeted-------------'


## bought Foreign
necessary = ['富蘭克林坦伯頓全球投資系列-全球平衡基金美元A(Qdis)股','富達基金－新興歐非中東基金(美元)','富蘭克林坦伯頓全球投資系列-亞洲成長基金美元A(Ydis)股','富蘭克林坦伯頓全球投資系列－全球債券總報酬基金美元A(acc)股']

for name in necessary:
	ma_dict, df_period, df_short = f.MA(name,three_year)
	f.plot_line(name,name,df_period,df_short,'Foreign/output/observation')
