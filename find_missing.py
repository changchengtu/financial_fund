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
missing_n = []
for n in names:
	tmp_list = tmp[n]
	state = False
	for v in tmp_list:
		if str(v) != 'nan':
			state=True
	if not state:
		print n
		missing_n.append(n)
print len(missing_n)
