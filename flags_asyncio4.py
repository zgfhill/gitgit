import asyncio, aiohttp, tqdm

from flags import BASE_URL,save_flag,show,main

@asyncio.coroutine
def get_flag(cc):
	url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
	img = yield from http_get(url)
	return img

@asyncio.coroutine
def http_get(url):
	res = yield from aiohttp.ClientSession().get(url)
	ctype = res.headers.get('Content-type','').lower()
	if 'json' in ctype or url.endswith('json'):
		data = yield from res.json()
	else:
		data = yield from res.read()
	return data

@asyncio.coroutine
def get_country(cc):
	url = '{}/{cc}/metadata.json'.format(BASE_URL,cc=cc.lower())
	metadata = yield from http_get(url)
	return metadata['country']

@asyncio.coroutine
def download_one(cc):
	image = yield from get_flag(cc)
	country = yield from get_country(cc)
	show(cc)
	filename = '{} - {}.gif'.format(country,cc)
	save_flag(image,filename)
	return cc

@asyncio.coroutine
def download_coro(cc_list):
	semaphore = asyncio.Semaphore(1)
	to_do=[download_one(cc) for cc in sorted(cc_list)]
	result = set()
	to_do_iter = tqdm.tqdm(asyncio.as_completed(to_do),total = 20)
	for future in to_do_iter:
		print(future)
		res = yield from future
		print(res)
		result.add(res)
	return result


def download_many(cc_list):
	loop = asyncio.get_event_loop()
	result = loop.run_until_complete(download_coro(cc_list))
	loop.close()
	return len(result)

if __name__=='__main__':
	main(download_many)

