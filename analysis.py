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

## remove legacy folders
current_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
for path, subdirs, files in os.walk(current_folder+'/Taiwan/output'):
	for folder_name in subdirs:
		shutil.rmtree(current_folder+'/Taiwan/output/'+folder_name)
		os.mkdir(current_folder+'/Taiwan/output/'+folder_name)

## remove legacy folders
current_folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
for path, subdirs, files in os.walk(current_folder+'/Foreign/output'):
	for folder_name in subdirs:
		shutil.rmtree(current_folder+'/Foreign/output/'+folder_name)
		os.mkdir(current_folder+'/Foreign/output/'+folder_name)



def BIAS_ratio(name_list, df, threshold):
	bias_dict = {}
	for name in name_list:
		try:
			ma_dict, df_period, df_short = f.MA(name,df)
		except:
			continue
		## seasonal BIAS
		slope_rate = -0.03
		if ma_dict['lon_s']>slope_rate and ma_dict['lon_going_up']:
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


print '\n-------------Taiwan-------------'

two_year = f.getTaiwanData(25)
six_m = f.getTaiwanData(6)
three_m = f.getTaiwanData(3)

nameT_list = six_m.columns.tolist()
nameT_list.remove('日期')


## classify funds
indexT_list = [ n for n in nameT_list if '指數' in n or 'ETF' in n or '台灣50' in n]
interestT_list = [ n for n in nameT_list if '配息' in n or '月配' in n or '年配' in n]
currencyT_list = [ n for n in nameT_list if '貨幣' in n]
bondT_list = [ n for n in nameT_list if '債卷' in n]
stockT_list = list(set(nameT_list)-set(currencyT_list)-set(interestT_list)-set(indexT_list)-set(bondT_list))



print '--index--'

biasT_rate_dict = BIAS_ratio(indexT_list, two_year, 0)
top_N_bias(biasT_rate_dict, two_year, 'Taiwan/output/index', 40)


print '--stock--'

biasT_rate_dict = BIAS_ratio(stockT_list, two_year, -3)
## top N bias
top_N_bias(biasT_rate_dict, two_year, 'Taiwan/output/stock', 40)


print '\n-------------Foreign-------------'

three_year = f.getForeignData(36)
six_m = f.getForeignData(6)
three_m = f.getForeignData(3)
	
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

attr = cat_df.columns.tolist()
for index, row in cat_df.iterrows():
	try:
		if '股票型' in row[attr[2]]:
			stockF_list.append(f.text_clean(row[attr[0]]))
		elif '固定收益型' in row[attr[2]]:
			bondF_list.append(f.text_clean(row[attr[0]]))
		elif '指數' in row[attr[2]]:
			indexF_list.append(f.text_clean(row[attr[0]]))
		elif '貨幣市場型' in row[attr[2]]:
			currencyF_list.append(f.text_clean(row[attr[0]]))
		elif '平衡型' in row[attr[2]]:
			balanceF_list.append(f.text_clean(row[attr[0]]))
		else:
			otherF_list.append(f.text_clean(row[attr[0]]))
	except:
		print attr[2], attr[0], row[attr[2]], row[attr[0]]


'''
'''
print '--index--'
biasF_rate_dict = BIAS_ratio(indexF_list, three_year, 20)
## top N bias
top_N_bias(biasF_rate_dict, three_year, 'Foreign/output/index', 60)
'''
'''
print '--stock--'
biasF_rate_dict = BIAS_ratio(stockF_list, three_year, -4)
## top N bias
top_N_bias(biasF_rate_dict, three_year, 'Foreign/output/stock', 60)


print '--balance--'
biasF_rate_dict = BIAS_ratio(balanceF_list, three_year, 0)
## top N bias
top_N_bias(biasF_rate_dict, three_year, 'Foreign/output/balance', 60)


print '--bond--'
biasF_rate_dict = BIAS_ratio(bondF_list, three_year, 0)
## top N bias
top_N_bias(biasF_rate_dict, three_year, 'Foreign/output/bond', 60)




print '-------------bought-------------'

## bought Taiwan
two_year = f.getTaiwanData(25)
necessary = ['復華全球資產證券化基金A','群益印度中小基金','群益印度中小基金',
			'德盛安聯中國東協新世紀基金','德盛安聯全球油礦金趨勢基金','第一金全球大趨勢基金','瀚亞巴西基金']

for name in necessary:
	ma_dict, df_period, df_short = f.MA(name,two_year)

	f.plot_line(name,name,df_period,df_short,'Taiwan/output/bought')

## bought Foreign
three_year = f.getForeignData(36)
necessary = ['富蘭克林坦伯頓全球投資系列-全球平衡基金美元A(Qdis)股','富達基金－新興歐非中東基金(美元)','富蘭克林坦伯頓全球投資系列-亞洲成長基金美元A(Ydis)股']

for name in necessary:
	ma_dict, df_period, df_short = f.MA(name,three_year)

	f.plot_line(name,name,df_period,df_short,'Foreign/output/bought')
