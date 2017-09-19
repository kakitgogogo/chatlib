from chatlib import *

c = chater()
logger = logging.getLogger('wechat')

f = open('birthtab.txt')
for row in f.readlines():
	s = row.strip().split(' ')
	print(s)
f.close()

while True:
	tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1), hour=0, minute=0, second=0)
	delta = tomorrow - datetime.datetime.now() + datetime.timedelta(seconds=5)
	logger.info('sleep time:'+str(delta))
	time.sleep(delta.total_seconds())
	f = open('birthtab.txt')
	for row in f.readlines():
		s = row.strip().split(' ')
		if int(s[0]) == tomorrow.month and int(s[1]) == tomorrow.day:
			c.chat(s[2], s[2]+'~生日快乐/:cake/:cake/:cake')
	f.close()