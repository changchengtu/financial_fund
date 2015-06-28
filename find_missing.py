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

six_m = f.getForeignData(36)
tmp = six_m.loc[(six_m['日期']<'2015-06-03'),:]
names = tmp.columns.tolist()

exception = ['鋒裕基金-亞洲股票(不含日本)U2','鋒裕基金-新興市場債券A2','鋒裕基金-新興歐洲及地中海股票U2',
			'鋒裕基金-新興歐洲及地中海股票U2(歐元)','鋒裕基金-核心歐洲股票A2(歐元)','鋒裕基金-歐洲潛力A2','鋒裕基金-環球生態U2',
			'鋒裕基金-美元短期債券U2','鋒裕基金-新興市場債券T2(歐元)','鋒裕基金-新興市場當地貨幣債券UXD','匯豐環球投資基金-巴西股票ID',
			'匯豐環球投資基金-歐元區股票ID','匯豐環球投資基金-歐洲股票ID','匯豐環球投資基金-環球債券IC',
			'霸菱德國增長基金- A類美元避險累積型','霸菱俄羅斯基金-A類美元累積型','霸菱德國增長基金- A類美元避險累積型']

missing_n = []
for n in names:
	if n in exception:
		continue
	tmp_list = tmp[n]
	state = False
	for v in tmp_list:
		if str(v) != 'nan':
			state=True
	if not state:
		print n
		missing_n.append(n)
print len(missing_n)
