from gevent import monkey;monkey.patch_all()
import gevent
import requests

def get_url(url):
	response = requests.get(url)
	html = response.text
	return len(html)

g1 = gevent.spawn(get_url, 'http://www.baidu.com')
g2 = gevent.spawn(get_url, 'http://www.sogou.com')
g3 = gevent.spawn(get_url, 'http://www.taobao.com')
g4 = gevent.spawn(get_url, 'http://www.hao123.com')
g5 = gevent.spawn(get_url, 'http://www.cnblogs.com')
gevent.joinall([g1, g2, g3, g4, g5])
print(g1.value)
print(g2.value)
print(g3.value)
print(g4.value)
print(g5.value)