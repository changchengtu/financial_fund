#!/usr/bin/env python
# -*- coding: utf-8 -*-
def text_clean(text):
	text = text.replace('—','-')
	text = text.replace('）',')').replace('（','(')
	text = text.replace(' ','')
	text = text.replace('/',':')
	text = text.replace('.txt','')
	text = text.replace('.txt','')
	return text

a = '駿利資產管理基金-駿利靈活入息基金 A 股歐元累計 (對沖)'
b = '駿利資產管理基金-駿利靈活入息基金A股歐元累計(對沖)'

print text_clean(a)==b