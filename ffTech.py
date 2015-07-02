#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unidecode import unidecode 
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
from datetime import datetime, date
import MySQLdb
import numpy as np
import json
import urllib2
import MySQLdb
import pandas as pd
from sqlalchemy import create_engine
from dateutil.relativedelta import relativedelta
import urllib, urllib2, cookielib
import csv
import os
import calendar
import numpy
from ckip import CKIPSegmenter, CKIPParser

current_path = os.path.dirname(os.path.realpath(__file__))
today = datetime.today().date()
LaDate = str(today)

day = today.day
month = today.month
year = today.year

## get data
def get_index_today():
	fund_url = 'http://www.msci.com/webapp/indexperf/charts?indices=2713,C,30|77,C,30|2879,C,30|85,C,30|2880,C,30|66,C,30&startDate='+str(day)+'%20'+calendar.month_name[month][0:3]+',%202012&endDate='+str(day)+'%20'+calendar.month_name[month][0:3]+',%20'+str(year)+'&priceLevel=0&currency=15&frequency=D&scope=R&format=CSV&baseValue=false&site=gimi'
	#print fund_url
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	resp = opener.open(fund_url)
	ori =  resp.read()
	data = ori.split('"')
	#print len(ori.split('"'))
	for i in range(len(ori.split('"'))):
		print data[2*i+1], data[2*i+2]
	
	#df = pd.DataFrame.from_csv(ori)
	#print df
	
	tmp_dict = {'日期':[],'Asia-SouthEast':[]}
	arr = tmp.split(',')
	for a in range(1,len(arr)/2):
		d = arr[2*a-1].split('/')[2]+'-'+arr[2*a-1].split('/')[0]+'-'+arr[2*a-1].split('/')[1]
		tmp_dict['日期'].append(d), tmp_dict['Asia-SouthEast'].append(arr[2*a])
	
	df = pd.DataFrame.from_dict(tmp_dict)
	
	## save file
	ma_dict, df_period = MA('Asia-SouthEast',df)
	long_df = df_period[df_period['日期']>str(today-relativedelta(months=24))]
	short_df = df_period[df_period['日期']>str(today-relativedelta(months=3))]
	plot_line('Asia-SouthEast',long_df,short_df, 'index')
	

	#return df

def getTaiwanData(period):
	df_curr = pd.read_csv('Taiwan//all-Taiwan-df.csv')

	# period months
	period_mons = today-relativedelta(months=period)
	df_period = df_curr[df_curr['日期']>str(period_mons)]

	return df_period


def getForeignData(period):
	df_curr = pd.read_csv('Foreign/all-Foreign-df.csv')

	# period months
	period_mons = today-relativedelta(months=period)
	df_period = df_curr[df_curr['日期']>str(period_mons)]

	return df_period


def trendline(df_period):
	#print '-------------------------'
	#print 'trendline'
	#print '-------------------------'
	results = {}
	df_period['id'] = df_period.index

	# all funds' names
	cols = df_period.columns.tolist()[1:]

	## for each fund
	for c in cols:
		try:
			model = pd.ols(y=df_period[c], x=df_period['id'], intercept=True)
			results[c] = model.beta.x
		except:
			#print c, 'is out'
			None

	return results

def drop(df_period, c):
	results = {}

	# max value
	period_max_dict = dict(df_period.max(axis=0))

	## for each fund

	period_max_value = float(period_max_dict[c])
	try:
		latest_value = float(df_period[c][pd.notnull(df_period[c])].iloc[-1])
		drop_percentage = (latest_value - period_max_value)/period_max_value
		results[c] = drop_percentage
	except:	
		results[c]=None

	return results

## diference between average and the latest value
def avgLow(df_period):
	print '-------------------------'
	print 'avgLow'
	print '-------------------------'
	results = {}
	# all funds' names
	cols = df_period.columns.tolist()[1:]

	# mean value
	period_mean_dict = dict(df_period.mean(axis=0))


	## for each fund
	for c in cols:
		#print c
		#for name in period_mean_dict:
		#	print name 
		#print period_mean_dict
		#period_mean_value = float(period_mean_dict[c])
		try:
			period_mean_value = float(period_mean_dict[c])
			latest_value = float(df_period[c][pd.notnull(df_period[c])].iloc[-1])
			avgLow_percentage = (latest_value - period_mean_value)/period_mean_value
			results[c] = float(int(avgLow_percentage*1000))/10
		except:	
			#print c, 'is out'
			None

	return results

def divide_df(name, df_period, days1=5, days2=20, days3=60):

	shortT = str(days1)+'MA'
	medianT = str(days2)+'MA'
	longT = str(days3)+'MA'

	## long term growrate
	ini = df_period.dropna().iloc[0][name]

	df_period[name+'-perf'] = ((df_period[name]-ini)/ini)*100
	df_period[shortT+'-perf'] = pd.rolling_mean(df_period[name+'-perf'], window=days1, min_periods=days1-1)
	df_period[medianT+'-perf'] = pd.rolling_mean(df_period[name+'-perf'], window=days2, min_periods=days2-3)
	df_period[longT+'-perf'] = pd.rolling_mean(df_period[name+'-perf'], window=days3, min_periods=days3-6)
	df_period[shortT] = pd.rolling_mean(df_period[name], window=days1, min_periods=days1-1)
	df_period[medianT] = pd.rolling_mean(df_period[name], window=days2, min_periods=days2-3)
	df_period[longT] = pd.rolling_mean(df_period[name], window=days3, min_periods=days3-6)


	## seasonal BIAS for long-term
	df_period['bias'] = (df_period[name]-df_period[longT])/df_period[longT]
	df_period['bias_abs'] = (df_period['bias']**2)**(0.5)
	## seasonal BIAS average
	df_period['moving_bias'] = pd.rolling_mean(df_period['bias_abs'], window=days3, min_periods=days3-6)
	df_period['moving_bias'] = df_period['moving_bias']*100
	df_period['60MA-perf-addSTD'] = df_period['60MA-perf']+df_period['moving_bias']
	df_period['60MA-perf-minusSTD'] = df_period['60MA-perf']-df_period['moving_bias']

	## short term growrate
	short_df = df_period[df_period['日期']>str(today-relativedelta(months=3))]
	ini_perf = short_df.dropna().iloc[0][name+'-perf']
	ini_short = short_df.dropna().iloc[0][name]

	## a,b,c -> (((c-a)/a-(b-a)/a)*a)b = (c-b)/b
	short_df[name+'-perf'] = ((short_df[name+'-perf']-ini_perf)*ini)/ini_short
	short_df[shortT+'-perf'] = ((short_df[shortT+'-perf']-ini_perf)*ini)/ini_short
	short_df[medianT+'-perf'] = ((short_df[medianT+'-perf']-ini_perf)*ini)/ini_short
	short_df[longT+'-perf'] = ((short_df[longT+'-perf']-ini_perf)*ini)/ini_short

	## seasional BIAS for short-term
	short_df['bias'] = (short_df[name]-short_df[longT])/short_df[longT]
	short_df['bias_abs'] = (short_df['bias']**2)**(0.5)
	bias_avg_short = float(int((short_df['bias_abs'].mean(axis=0))*1000))/10
	short_df['60MA-perf-addSTD'] = short_df['60MA-perf']+bias_avg_short 
	short_df['60MA-perf-minusSTD'] = short_df['60MA-perf']-bias_avg_short 

	return df_period, short_df


## moving average
def MA(name, df_period, days1=5, days2=20, days3=60):

	shortT = str(days1)+'MA'
	medianT = str(days2)+'MA'
	longT = str(days3)+'MA'

	df_period = df_period[['日期',name]]
	df_period, short_df = divide_df(name, df_period, days1, days2, days3)

	## calculate slope changes
	days = 5
	tmp_df = df_period.iloc[-days:]
	tmp_df['id'] = tmp_df.index
	pre_tmp_df = df_period.iloc[-2*days:-days]
	pre_tmp_df['id'] = pre_tmp_df.index

	## short term slope
	latest_short = pd.ols(y=tmp_df[shortT], x=tmp_df['id'], intercept=True)
	short_slope = latest_short.beta.x

	## median term slope ##################
	latest_median = pd.ols(y=tmp_df[medianT], x=tmp_df['id'], intercept=True)
	median_slope = latest_median.beta.x
	## slope comparision
	pre_median = pd.ols(y=pre_tmp_df[medianT], x=pre_tmp_df['id'], intercept=True)
	pre_median_slope = pre_median.beta.x
	mid_going_up = False
	if pre_median_slope<median_slope:
		mid_going_up = True
	######################################

	## long term slope ####################
	latest_long = pd.ols(y=tmp_df[longT], x=tmp_df['id'], intercept=True)
	long_slope = latest_long.beta.x
	## slope comparision
	pre_long = pd.ols(y=pre_tmp_df[longT], x=pre_tmp_df['id'], intercept=True)
	pre_long_slope = pre_long.beta.x
	lon_going_up = False
	if pre_long_slope<long_slope:
		lon_going_up = True
	######################################

	## latest value
	ori = df_period[name].iloc[-1]
	sho = df_period[shortT].iloc[-1]
	med = df_period[medianT].iloc[-1]
	lon = df_period[longT].iloc[-1]

	pre_bias_v = float(int((df_period['bias'].dropna().iloc[-1])*1000))/10



	return_dict = {
		'sho_s':short_slope,
		'med_s':median_slope,
		'lon_s':long_slope,
		'ori_v':ori,
		'sho_v':sho,
		'med_v':med,
		'lon_v':lon,
		'mid_going_up': mid_going_up,
		'lon_going_up': lon_going_up,
		'pre_bias_v': pre_bias_v,
	}

	#print df_period
	return return_dict, df_period, short_df



def plot_line(fund_name, png_name, df_long,df_short, folder):
	plt.figure()
	###

	df_long = df_long.rename(columns={fund_name:'original',fund_name+'-perf':'original-perf'})
	df_short = df_short.rename(columns={fund_name:'original',fund_name+'-perf':'original-perf'})

	y_arr = ['original','5MA','20MA','60MA']
	y_arr_perf = ['original-perf','5MA-perf','20MA-perf','60MA-perf','60MA-perf-addSTD','60MA-perf-minusSTD']

	## subplot set
	fig, axes = plt.subplots(nrows=2, ncols=2,sharex=False, figsize=(16,8))

	ax_long = df_long.plot(kind='line',
			y = y_arr,
		   	x = ['日期'],
		   	ax = axes[0,0],
		   	title = 'long term net value'
			)
	ax_long_perf = df_long.plot(kind='line',
			y = y_arr_perf,
		   	x = ['日期'],
		   	ax = axes[1,0],
		   	title = 'long term performance'
			)
	ax_short = df_short.plot(kind='line',
			y = y_arr,
		   	x = ['日期'],
		   	ax = axes[0,1],
		   	title = 'short term net value'
			)
	ax_short_perf = df_short.plot(kind='line',
			y = y_arr_perf,
		   	x = ['日期'],
		   	ax = axes[1,1],
		   	title = 'short term performance'
			)

	plt.setp(ax_long.get_xticklabels(), visible=True, rotation=10, horizontalalignment='right')
	plt.setp(ax_short.get_xticklabels(), visible=True, rotation=10, horizontalalignment='right')
	plt.setp(ax_long_perf.get_xticklabels(), visible=True, rotation=10, horizontalalignment='right')
	plt.setp(ax_short_perf.get_xticklabels(), visible=True, rotation=10, horizontalalignment='right')
	
	fig.savefig(current_path+'/'+folder+'/'+png_name+'.png')
	plt.close('all')

def get_hot_term(string):
	segmenter = CKIPSegmenter('changcheng.tu', 'a10206606')
	trash_words = ['摩根','富蘭克林坦伯頓','優勢','國','富達','德盛',
					'基金','勢力','世紀','瀚亞','德盛德利','金','全方位',
					'霸菱','單位','系列','安聯','元','施羅德','巴百','柏瑞'
					'利達','主題','收益','累積型','股','國','新光','股份','幣'
					'小型','利達','國家','投資','趨勢','柏瑞','市場','歐','法',
					'英鎊','美元','景順','標智','盧森堡','保德信','集團','上證'
					'國際','寶盛','機會']
	hot_words = []
	try:
		segmented_result = segmenter.process(string.decode('utf-8'))
		for row in segmented_result['result'][0]:
			if row['pos']=='N':
				if row['term'] not in trash_words:
					hot_words.append(row['term'])
	except:
		print string, 'can not be decode'
	return hot_words

def nameF_dict():
	tmp_dict = {}
	for row in csv.DictReader(open('codeF_name.txt','rb')):
		tmp_dict[row['code']] = row['name']
	return tmp_dict

def nameT_dict():
	tmp_dict = {}
	for row in csv.DictReader(open('codeT_name.txt','rb')):
		tmp_dict[row['code']] = row['name']
	return tmp_dict

def text_clean(text):
	text = text.replace('—','-')
	text = text.replace('）',')').replace('（','(')
	text = text.replace(' ','')
	text = text.replace('/','-')
	return text


