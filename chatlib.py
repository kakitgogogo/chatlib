from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import *
import time, datetime
import platform
import logging

sysstr = platform.system()

logger = logging.getLogger('wechat')

logging.basicConfig(level=logging.INFO, 
					format='[%(asctime)s] %(message)s',
					datefmt='%d %b %Y %H:%M:%S',
					filename='log.txt',
					filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

class chater:
	def __init__(self):
		self.url = 'https://wx.qq.com/'
		if sysstr == 'Windows':
			self.driver = webdriver.Chrome()
		elif sysstr == 'Linux':
			self.driver = webdriver.PhantomJS()
		else:
			logger.warning("I don't know how to use other systems")
			exit()
		self.login()

	def findElement(self, css, idx=0, cnt=5, interval=1):
		while cnt > 0:
			l = self.driver.find_elements_by_css_selector(css)
			if len(l) > 0:
				return l[idx]
			time.sleep(interval)
			cnt = cnt - 1
		return None

	def login(self):	
		self.driver.get(self.url)
		img = self.findElement('img[class="img"]')
		logger.info(img.get_attribute('src'))
		if not self.findElement('span[class="nickname_text ng-binding"]', cnt=100):
			logger.error('login failed')
			exit()
		logger.info('login success')

	def getTalkingList(self):
		return self.driver.find_elements_by_css_selector('span[class="nickname_text ng-binding"]')

	def searchFriendByScroll(self, name):
		self.driver.find_element_by_css_selector('div[class="tab_item no_extra"]').click()
		preButtonName = ''
		curButtonName = ' '
		chain = None
		while preButtonName != curButtonName:
			items = self.driver.find_elements_by_css_selector('h4[class="nickname ng-binding"]')
			for item in items:
				if name in item.text:
					item.click()
					self.driver.find_element_by_css_selector('a[ui-sref="chat({userName:user.UserName})"]').click()
					return True
			preButtonName = curButtonName
			curButtonName = items[-1].text
			if chain == None:
				chain = ActionChains(self.driver)
				chain.move_to_element(items[0]).perform()
				for i in range(0,15):
					chain.key_down(Keys.DOWN).perform()
			for i in range(0,15):
				chain.key_down(Keys.DOWN).perform()

		return False

	def searchFriend(self, name):
		searchBox = self.driver.find_element_by_css_selector('input[placeholder="Search"]')
		searchBox.clear()
		searchBox.send_keys(name)
		time.sleep(1)
		searchBox.send_keys(Keys.ENTER)
		return True

	def chat(self, name, content):
		ret = self.searchFriend(name)
		if ret:
			editArea = self.driver.find_element_by_id('editArea')
			editArea.click()
			editArea.send_keys(content)
			editArea.send_keys(Keys.ENTER)
			return True
		return False

