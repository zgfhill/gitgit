import os,sys,time,requests

POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()

BASE_URL = 'http://flupy.org/data/flags'

DEST_DIR = 'flagy/'

def save_flag(img,filename):
	path = os.path.join(DEST_DIR, filename)
	with open(path,'wb') as fp:
		fp.write(img)

def show(text):
	print(text,end=' ')
	sys.stdout.flush()

def get_flag(cc):
	url = '{}/{cc}/{cc}.gif'.format(BASE_URL,cc=cc.lower())
	image = requests.get(url)
	return image.content

def download_many(cc_list):
	for cc in sorted(cc_list):
		img=get_flag(cc)
		show(cc)
		save_flag(img, cc+'.gif')
	return len(cc_list)

def main(download_many):
	t0 = time.time()
	result=download_many(POP20_CC)
	elapsed = time.time() -t0
	print('{} flags downloaded in {:.2f}'.format(result,elapsed))

	main(download_many)
