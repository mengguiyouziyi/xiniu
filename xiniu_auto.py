import time
import pymysql
from selenium import webdriver
from scrapy import Selector
from urllib.parse import urljoin

try:
	"""本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org"""
	mysql = pymysql.connect(host='etl2.innotree.org', port=3308, user='spider', password='spider', db='spider', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	# mysql = pymysql.Connect(host='localhost', port=3308, user='root', password='3646287', db='spiders', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

	url1 = "http://www.xiniudata.com/#/discover"
	url = "http://www.xiniudata.com/account/#/"
	base_url = 'http://www.xiniudata.com'

	# 设置chromedriver不加载图片
	chrome_opt = webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.images": 2}
	chrome_opt.add_experimental_option("prefs", prefs)
	browser = webdriver.Chrome(executable_path='/Users/menggui/Downloads/chromedriver', chrome_options=chrome_opt)

	browser.get(url)
	browser.find_element_by_id('username').send_keys(13784855457)
	browser.find_element_by_id('password').send_keys(3646287)
	browser.find_element_by_class_name('btn-confirm').click()
	time.sleep(2)
	browser.get(url1)
	time.sleep(5)
	browser.find_element_by_xpath('//div[@class="funding-topic"]/div[2]').click()
	time.sleep(3)

	for i in range(60):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		time.sleep(1)
	# with open('a.html', 'a') as f:
	# 	f.write(browser.page_source)

	sele = Selector(text=browser.page_source)

	list_div = sele.xpath('//div[@class="list-by-date"]/div')
	counts = 0
	for div in list_div:
		list_sort_date = div.xpath('./div[@class="list-sort-date"]//text()').extract_first().strip()
		items = div.xpath('./div[@class="company-item company-item-v2"]')
		for item in items:
			counts += 1
			item_id = item.xpath('./@id').extract_first()
			item_name = item.xpath('.//div[contains(@class, "item-name")]/a//text()').extract_first()
			item_url_un = item.xpath('.//div[contains(@class, "item-name")]/a/@href').extract_first()
			item_url = urljoin(base_url, item_url_un)
			item_description = item.xpath('.//div[@class="item-description"]//text()').extract_first()
			item_round = item.xpath('.//span[@class="item-round"]//text()').extract_first()
			item_establishDate = item.xpath('.//span[@class="item-establishDate"]//text()').extract_first()
			item_location_un = item.xpath('.//span[@class="item-location"]//text()').extract()
			item_location = item_location_un[1] if item_location_un else ''

			print(counts, list_sort_date, item_id, item_name, item_url, item_description, item_round,
			      item_establishDate, item_location)

			with mysql.cursor() as cursor:
				sql = """replace into xiniu_funding (list_sort_date, item_id, item_name, item_url, item_description, item_round, item_establishDate, item_location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
				args = (
					list_sort_date, item_id, item_name, item_url, item_description, item_round, item_establishDate,
					item_location)
				cursor.execute(sql, args)
				mysql.commit()
except Exception as e:
	print(e)
finally:
	mysql.close()
	browser.quit()
