
def html(get_url):
	def inner(a):
		print(1,'='*a)
		get = get_url()
		return get
	return inner

@html#get_url = html(get_url):=inner
def get_url():
	print(2)

get_url(5)
