import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool
from multiprocessing import Process
import json
#from fake_useragent import UserAgent
import re
import os
import datetime
import urllib.request
import time

#开启多线程
# def thread(func):
# 	def inner(args):
# 		tpool = ThreadPoolExecutor(max_workers=5)
# 		get = tpool.submit(func, args)
# 		tpool.shutdown()
# 		#get = func(args)
# 		return get.result()
# 	return inner

#开启多进程
def process(func):
	def inner(args):
		ppool = ProcessPoolExecutor(max_workers=3)
		get = ppool.submit(func, args)
		ppool.shutdown()
		# get = func(args)
		return get.result()
	return inner


@process
def open_show_url(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}

	response = requests.get(url, headers = headers)
	html = response.content
	# req = urllib.request.Request(url)
	# #req.add_header('User-Agent', agent)
	# req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36')
	# response = urllib.request.urlopen(req)
	# html = response.read()
	
	return html


@process
def open_detail_url(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
	response = urllib.request.urlopen(req)
	html = response.read()
	return html


def find_show_url(html):
	#print('findurl')
	# TBshow = re.compile('<img data-src="(//gd\d\.alicdn\.com/imgextra.*?.jpg).*?".*?>')
	# TBdetail = re.compile('https://img\.alicdn\.com/imgextra/\w{2,4}/\d+/.*?\.jpg')
	# toTBdetail = re.compile('//desc\.alicdn\.com/\w{2,5}/\w{2,5}/\d+/\d+/TB.{20,28}\.desc%7Cvar%5Edesc%3Bsign%.*?%3Blang%5Egbk%3Bt%.{12}')

	pattern = re.compile(u'<ul id="J_UlThumb".*?>'
							+ '.*?<li.*?>.*?src="(.*?\.[jpg]{3}|[png]{3}).*?".*?</li>'
							+ '.*?<li.*?>.*?src="(.*?\.[jpg]{3}|[png]{3}).*?".*?</li>'
							+ '.*?<li.*?>.*?src="(.*?\.[jpg]{3}|[png]{3}).*?".*?</li>'
							+ '.*?<li.*?>.*?src="(.*?\.[jpg]{3}|[png]{3}).*?".*?</li>'
							+ '.*?<li.*?>.*?src="(.*?\.[jpg]{3}|[png]{3}).*?".*?</li>'
							+ '.*?</ul>',
							re.S)
	imgurl = pattern.findall(html)
	imglist = []
	print(imgurl)
	for each in imgurl[0]:
		imglist.append(each)
	#print('findurl-OK')
	#print(imglist)
	return imglist



def find_detail_url(html):
	#print(html)https://img.alicdn.com/imgextra
	pattern = re.compile('https://img.alicdn.com/imgextra/.*?/.*?/.*?\.[jpgpng]{3}|//gdp.*?/.*?/.*?/.*?/.*?\.[jpgpng]{3}')
	imgurl = pattern.findall(html)
	imglist = list(set(imgurl))
	imglist.sort(key = imgurl.index)
	print(imglist)
	return imglist


def saveimg(img, filename):
		with open('%s'%filename, 'wb') as f:
			f.write(img)



def checkurl(imglist):
	for each in imglist:
		index = imglist.index(each)
		if 'http' not in each:
			each = 'http:' + each
		yield each, index


def main():
	time = datetime.datetime.now().strftime('%Y-%m-%d')
	trunk = os.getcwd() + '\\' + time
	if os.path.exists(trunk) == False:
		os.mkdir(trunk)
	os.chdir(trunk)

	parentalfile = input('文件名:')
	#url = input('网址:')
	url = 'https://item.taobao.com/item.htm?spm=a219r.lm5704.14.28.7c9120e9BOtFWk&id=571227239859&ns=1&abbucket=9#detail'
	filename = ['五张展示图', '详情页图片']
	filenum = len(filename)



	showhtml = open_show_url(url).decode('GBK', errors = 'ignore')#decode('utf-8', errors='ignore')
	detailhtml = open_detail_url(url).decode('GBK', errors = 'ignore')
	ShowImg = find_show_url(showhtml)
	DetailImg = find_detail_url(detailhtml)
	imggroup = [ShowImg, DetailImg]

	os.mkdir(parentalfile)
	os.chdir(parentalfile)

	while filenum:
		filenum -= 1
		os.mkdir(filename[filenum])
		os.chdir(filename[filenum])
		for each, index in checkurl(imggroup[filenum]):
			img = open_show_url(each)
			imgname = str(index) + each[-4:]
			saveimg(img, imgname)
		os.chdir(os.path.dirname(os.getcwd()))


if __name__ == '__main__':
		start = time.time()
		main()
		end = time.time() - start
		print(end)