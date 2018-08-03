from concurrent.futures import ThreadPoolExecutor

def func(n):
	print(n)
	return '============='

if __name__ == '__main__':
	tpool = ThreadPoolExecutor(max_workers=5)
	for each in range(200):
		t = tpool.submit(func, each)
	
		#t_list.append(t)
	tpool.shutdown()
	print(t.result())
	
	#for each in t_list:print(each.result())
	#print('主线程')

# for i in range(200):
# 	print(i**i)
