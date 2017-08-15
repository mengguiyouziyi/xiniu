import time
import pymysql
from selenium import webdriver
from scrapy import Selector
from urllib.parse import urljoin

# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H8J738EHR4H5GE5D"
proxyPass = "3018672C5A167A3D"

service_args = [
	"--proxy-type=http",
	"--proxy=%(host)s:%(port)s" % {
		"host": proxyHost,
		"port": proxyPort,
	},
	"--proxy-auth=%(user)s:%(pass)s" % {
		"user": proxyUser,
		"pass": proxyPass,
	},
]

try:
	"""本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org"""
	mysql = pymysql.connect(host='etl2.innotree.org', port=3308, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	# mysql = pymysql.Connect(host='localhost', port=3308, user='root', password='3646287', db='spiders', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	cursor = mysql.cursor()
	sql = """select item_name, item_url from xiniu_funding_copy """
	cursor.execute(sql)
	items = cursor.fetchall()

	# items = [
	# 	{'item_name': 'X-legal', 'item_url': 'http://www.xiniudata.com/#/company/X-legal/overview'},
	# 	{'item_name': '猿题库', 'item_url': 'http://www.xiniudata.com/#/company/yuantiku6/overview'},
	# 	# {'item_name': '集餐厨直卖网', 'item_url': 'http://www.xiniudata.com/#/company/WD0VS6QW/overview'},
	# 	# {'item_name': '玉米社群', 'item_url': 'http://www.xiniudata.com/#/company/yumishequn/overview'},
	# 	# {'item_name': '吃个汤', 'item_url': 'http://www.xiniudata.com/#/company/chigetang/overview'},
	# 	# {'item_name': '启纬智芯', 'item_url': 'http://www.xiniudata.com/#/company/3A7P3GYP/overview'},
	# ]
	url = "http://www.xiniudata.com/account/#/"
	url1 = "http://www.xiniudata.com/#/discover"
	base_url = 'http://www.xiniudata.com'

	# 设置chromedriver不加载图片
	# chrome_opt = webdriver.ChromeOptions()
	# prefs = {"profile.managed_default_content_settings.images": 2}
	# chrome_opt.add_experimental_option("prefs", prefs)
	browser = webdriver.Chrome(executable_path='/Users/menggui/Downloads/chromedriver')

	browser.get(url)

	time.sleep(10)
	print(browser.page_source)
	# with open('x.html', 'a') as f:
	# 	f.write(browser.page_source)

	browser.find_element_by_id('username').send_keys(13784855457)
	browser.find_element_by_id('password').send_keys(3646287)
	browser.find_element_by_class_name('btn-confirm').click()
	time.sleep(3)

	for item in items:
		item_name = item['item_name']
		item_url = item['item_url']

		browser.get(item_url)
		time.sleep(30)
		# if Selector(text=browser.page_source).xpath('//div[@class="content"]//a[@class="a-button a-extend"]').extract():
		# 	browser.execute_script("var q=document.documentElement.scrollTop=200")
		# 	time.sleep(3)
		# 	browser.find_element_by_id('basicInfo').find_element_by_class_name('a-button').click()
		# 	time.sleep(5)

		sele = Selector(text=browser.page_source)
		website = sele.xpath('//a[@class="website"]/@href').extract_first()
		brief = sele.xpath('//div[@class="brief"]/span//text()').extract_first()
		company = sele.xpath('//div[@class="gongshangs"]/span//text()').extract_first()
		tags_list = sele.xpath('//span[@class="tag-border"]//text()').extract()  # not
		tags = str(tags_list)
		des = sele.xpath('//div[@class="desc inner-scroll"]/pre//text()').extract_first()

		funding_items = sele.xpath('//div[@class="funding-item"]')
		funding_list = []  # not
		for funding in funding_items:
			fund_date = funding.xpath('./div[@class="date"]/text()').extract_first()
			fund_round = funding.xpath('./div[@class="round"]/text()').extract_first()
			fund_investment = funding.xpath('./div[@class="investment"]//text()').extract_first()
			fund_com_str = funding.xpath('./div[@class="investors"]//text()').extract()  # todo
			fund_com_url_obj = funding.xpath('.//a[@class="investor-a"]')
			com_url_list = []
			if fund_com_url_obj:
				for fund_com_url in fund_com_url_obj:
					com_text = fund_com_url.xpath('.//text()').extract_first()
					a_url = fund_com_url.xpath('./@href').extract_first()
					url_a = a_url if a_url else ''
					com_url_list.append({'com_text': com_text, 'url_a': url_a})
			com_url = str(com_url_list)
			source_text = funding.xpath('./div[@class="source"]//a//text()').extract_first()
			source_url_un = funding.xpath('./div[@class="source"]//a/@href').extract_first()
			source_url = urljoin(base_url, source_url_un) if source_url_un else source_url_un
			funding_list.append(
				{'fund_date': fund_date, 'fund_round': fund_round, 'fund_investment': fund_investment,
				 'fund_com_str': fund_com_str,
				 'com_url': com_url, 'source_text': source_text, 'source_url': source_url})
		fundings_str = str(funding_list)
		print(item_name, website, brief, company, tags, des, fundings_str)

		# sql = """replace into xiniu_funding (item_name, website, brief, company, tags, des, fundings_str) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
		sql = """update xiniu_funding_copy set website=%s, brief=%s, company=%s, tags=%s, des=%s, fundings_str=%s where item_name=%s"""
		args = (website, brief, company, tags, des, fundings_str, item_name)
		cursor.execute(sql, args)
		mysql.commit()
except Exception as e:
	print(e)
finally:
	mysql.close()
	browser.quit()








# for i in range(60):
# 		browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# 		time.sleep(1)
# 	# with open('a.html', 'a') as f:
# 	# 	f.write(browser.page_source)
#
# 	sele = Selector(text=browser.page_source)
#
# 	list_div = sele.xpath('//div[@class="list-by-date"]/div')
# 	counts = 0
# 	for div in list_div:
# 		list_sort_date = div.xpath('./div[@class="list-sort-date"]//text()').extract_first().strip()
# 		items = div.xpath('./div[@class="company-item company-item-v2"]')
# 		for item in items:
# 			counts += 1
# 			item_id = item.xpath('./@id').extract_first()
# 			item_name = item.xpath('.//div[contains(@class, "item-name")]/a//text()').extract_first()
# 			item_url_un = item.xpath('.//div[contains(@class, "item-name")]/a/@href').extract_first()
# 			item_url = urljoin(base_url, item_url_un)
# 			item_description = item.xpath('.//div[@class="item-description"]//text()').extract_first()
# 			item_round = item.xpath('.//span[@class="item-round"]//text()').extract_first()
# 			item_establishDate = item.xpath('.//span[@class="item-establishDate"]//text()').extract_first()
# 			item_location_un = item.xpath('.//span[@class="item-location"]//text()').extract()
# 			item_location = item_location_un[1] if item_location_un else ''
#
# 			print(counts, list_sort_date, item_id, item_name, item_url, item_description, item_round,
# 			      item_establishDate, item_location)
#
# 			with mysql.cursor() as cursor:
# 			sql = """replace into xiniu_funding (list_sort_date, item_id, item_name, item_url, item_description, item_round, item_establishDate, item_location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
# 			args = (
# 				list_sort_date, item_id, item_name, item_url, item_description, item_round, item_establishDate,
# 				item_location)
# 			cursor.execute(sql, args)
# 			mysql.commit()
# except Exception as e:
# 	print(e)
# finally:
# 	mysql.close()
# 	browser.quit()
#
#
#
# finally:
# 	browser.quit()
