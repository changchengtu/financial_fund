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


hot_terms = []

print '-------------'
print 'Taiwan'
print '-------------'


two_year = f.getTaiwanData(24)
six_m = f.getTaiwanData(6)
three_m = f.getTaiwanData(3)

nameT_list = six_m.columns.tolist()
nameT_list.remove('日期')

longT_term_list = []
biasT_rate_dict = {}


## for loop is just for name list
for name in nameT_list:
	## (a year) if this fund is growing
	if '配息' in name or '貨幣' in name or '月配' in name or '年配' in name or '短期' in name:
		continue

	else:
		try:
			ma_dict, df_period, df_short = f.MA(name,two_year)
		except:
			continue

		high_bet_rate = 0.02

		## long term and median term go up
		long_slope_rate = -0.001
		mid_slope_rate = 0.001	
		if ma_dict['lon_s']>long_slope_rate and ma_dict['lon_going_up']:
			if ma_dict['med_s']>mid_slope_rate and ma_dict['mid_going_up']:
				if (ma_dict['med_v']-ma_dict['lon_v'])/ma_dict['lon_v'] < high_bet_rate:
					f.plot_line(name,name,df_period, df_short, 'Taiwan/output/long term')
					longT_term_list.append(name)


		## seasonal BIAS
		slope_rate = -0.001
		if ma_dict['lon_s']>slope_rate and ma_dict['lon_going_up']:
			if ma_dict['pre_bias_v'] < -4:
				biasT_rate_dict[name] = ma_dict['pre_bias_v']


## top N bias
sorted_biasT_rate_dict = dict(sorted(biasT_rate_dict.items(), key=operator.itemgetter(1), reverse=False)[:40])

for fund_name in sorted_biasT_rate_dict:
	print fund_name
	ma_dict, df_period, df_short = f.MA(fund_name,two_year)

	rate = sorted_biasT_rate_dict[fund_name]
	f.plot_line(fund_name, str(rate)+'-'+fund_name,df_period, df_short, 'Taiwan/output/BIAS')
	for t in f.get_hot_term(fund_name):
		hot_terms.append(t)

	if fund_name in longT_term_list:
		f.plot_line(fund_name, str(rate)+'-'+fund_name,df_period, df_short, 'Taiwan/output/long&BIAS')



print '-------------'
print 'Foreign'
print '-------------'

three_year = f.getForeignData(36)
six_m = f.getForeignData(6)
three_m = f.getForeignData(3)

	
nameF_list = six_m.columns.tolist()
nameF_list.remove('日期')

longF_term_list = []
biasF_rate_dict = {}
## 'for loop' is just for name list
for name in nameF_list:
		## (a year) if this fund is growing
	if '配息' in name or '貨幣' in name or '月配' in name or '年配' in name or '短期' in name:
		continue

	else:
		try:
			ma_dict, df_period, df_short = f.MA(name,three_year)
		except:
			continue

		high_bet_rate = 0.02
		## long term and median term go up
		long_slope_rate = -0.001
		mid_slope_rate = 0	
		if ma_dict['lon_s']>long_slope_rate and ma_dict['lon_going_up']:
			if ma_dict['med_s']>mid_slope_rate and ma_dict['mid_going_up']:
				if (ma_dict['med_v']-ma_dict['lon_v'])/ma_dict['lon_v'] < high_bet_rate:
					f.plot_line(name,name,df_period, df_short, 'Foreign/output/long term')
					longF_term_list.append(name)


		## seasonal BIAS
		slope_rate = -0.001
		if ma_dict['lon_s']>slope_rate and ma_dict['lon_going_up']:
			if ma_dict['pre_bias_v'] < -4:
				biasF_rate_dict[name] = ma_dict['pre_bias_v']


## top N bias
sorted_biasF_rate_dict = dict(sorted(biasF_rate_dict.items(), key=operator.itemgetter(1), reverse=False)[:60])
for fund_name in sorted_biasF_rate_dict:
	print fund_name

	ma_dict, df_period, df_short = f.MA(fund_name,three_year)

	rate = sorted_biasF_rate_dict[fund_name]
	f.plot_line(fund_name,str(rate)+'-'+fund_name, df_period, df_short, 'Foreign/output/BIAS')
	for t in f.get_hot_term(fund_name):
		hot_terms.append(t)

	if fund_name in longF_term_list:
		f.plot_line(fund_name, str(rate)+'-'+fund_name, df_period, df_short, 'Foreign/output/long&BIAS')


print '-------------'
print 'Total report'
print '-------------'

## hot terms
hot_terms = list(set(hot_terms))
tmp_str = ''
for s in hot_terms:
	tmp_str+=s+'\n'
open('hot_terms.txt', 'wr').write(tmp_str)
	

## bought Taiwan
two_year = f.getTaiwanData(24)
necessary = ['復華全球資產證券化基金A','群益印度中小基金','群益印度中小基金',
			'德盛安聯中國東協新世紀基金','德盛安聯全球油礦金趨勢基金','第一金全球大趨勢基金']

for name in necessary:
	ma_dict, df_period, df_short = f.MA(name,two_year)

	f.plot_line(name,name,df_period,df_short,'Taiwan/output/bought')

## bought Foreign
three_year = f.getForeignData(36)
necessary = ['富蘭克林坦伯頓全球投資系列-全球平衡基金美元A(Qdis)股','富達基金－新興歐非中東基金(美元)']

for name in necessary:
	ma_dict, df_period, df_short = f.MA(name,three_year)

	f.plot_line(name,name,df_period,df_short,'Foreign/output/bought')
