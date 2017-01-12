#!/usr/bin/env python
# -*- coding:utf-8-*-

import re
from lxml import html
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

loginData = {
	'app_code':'ECS-YH-WAP',
	'user_id':'PhoneNumber',
	'user_pwd':'Password',
	'redirect_uri':'http://wap.10010.com/t/loginCallBack.htm',
	'user_type':'01',
	'pwd_type':'01',
	'display':'web',
	'response_type':'code',
	'redirect_uri':'http://wap.10010.com/t/loginCallBack.htm',
	'is_check':'1',
	'state':'http://wap.10010.com/t/myunicom.htm'
	}
TimeOut = 5
header = {
	'Host': 'uac.10010.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'X-Requested-With': 'XMLHttpRequest',
	'Referer': 'https://uac.10010.com/oauth2/new_auth?display=wap&page_type=05&app_code=ECS-YH-WAP&redirect_uri=http://wap.10010.com/t/loginCallBack.htm&state=http://wap.10010.com/t/myunicom.htm&channel_code=113000001&real_ip=105.91.1.6',
	'Content-Length': '238',
	'Connection': 'close',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache'
	}
Cookie = {
	'route':'59dd262016757076d214a2c4de006e9f', 
	'mobileService':'5QJDY2QQDPSwnj23pRWrgNPntJhk6yGwwmdvPL6GLN6svhnJ90Ht!1280148686'
	}
proxies = {
  "http": "http://127.0.0.1:8888"
}

try:
	s = requests.Session()
	r=s.post('http://uac.10010.com/oauth2/new_auth',data=loginData, headers=header, timeout=TimeOut)
	data=json.loads(r.text)
	code=data['code']
	s.get('http://wap.10010.com/t/loginCallBack.htm?code={0}'.format(code))
	r=s.get('http://wap.10010.com/mobileService/query/getPhoneByDetailContent.htm')

	r.encoding = 'utf-8'
	content=r.text

	phone_reg=r'<table class="call_table call_table1">'
	phonelist=re.findall(phone_reg, content)
	
	tree = html.fromstring(content)
	date=tree.xpath('//table[@class="call_table call_table1"]//p[@class="time"]/text()')

	for i in xrange(0,len(phonelist)):
		# print '============[',i,']============\n'

		phone=tree.xpath('//table[@class="call_table call_table1"]//label[@class="telphone"]/text()')
		inout=tree.xpath('//table[@class="call_table call_table1"]//em/@class')
		duration=tree.xpath('//table[@class="call_table call_table1"]//p[@class="num col_fe7f05"]/text()')
		inout_str=inout[i].replace('call_img','').replace('mar_8','').strip().replace('call_out','呼出').replace('call_in','呼入')

		phone_str=phone[i]
		duration_str=duration[i]
		# date_str="".join(date[i+i+1].split()).encode('raw_unicode_escape')
		date_str="".join(date[i+i+1].split())
		fee_str=date[i+i]

# 			print '''
# [{0}] {1}
# [时长] {2}
# [日期] {3}
# [费用] {4}'''.format(inout_str, phone_str, duration_str, date_str, fee_str)
		
		print '\n[{0}] {1}\n[时长] {2}\n[日期] {3}\n[费用] {4}'.format(inout_str, phone_str, duration_str, date_str, fee_str)

		if i>6:
			exit()

except Exception as e:
	raise e
# except: pass
