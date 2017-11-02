# coding:utf-8
import json
import time
import requests
import pymysql
from traceback import print_exc
from urllib.parse import urljoin

base_url = 'http://www.xiniudata.com'

headers = {
	'host': "www.xiniudata.com",
	'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0",
	'accept': "*/*",
	'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	'accept-encoding': "gzip, deflate",
	'content-type': "application/json",
	'x-requested-with': "XMLHttpRequest",
	'referer': "http://www.xiniudata.com/",
	'content-length': "95",
	'cookie': "Hm_lvt_42317524c1662a500d12d3784dbea0f8=1502272135; Hm_lpvt_42317524c1662a500d12d3784dbea0f8=1502353879; gtserverstatus=1; gtuserid=8J6TPO8MIYYCTAHB; userid=5968; token=P8WPBUXJPG59K6CPT9FQ5H8ZJVRPBMF7; keeploginsecret=SRXEVRJ8AGDQI6IYXWF1S9D7U1DT87BW; location=http%3A%2F%2Fwww.xiniudata.com%2F%23%2Fdiscover",
	'connection': "keep-alive",
	'cache-control': "no-cache",
	'postman-token': "cf370e7f-d6ab-8672-0c13-de5d34594166"
}


def json_loop(tstamp, num, field):
	mysql = pymysql.connect(host='172.31.215.38', port=3306, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	cursor = mysql.cursor()

	url = "http://www.xiniudata.com/api2/service/x_service/system_discover_topic/list_funding_topic_company"
	payload = "{\"payload\":{\"topicId\":26,\"sectors\":[],\"publishTime\":%s,\"limit\":%s,\"isChina\":%s}}" % (str(
		tstamp), num, field)

	response = requests.request("POST", url, data=payload, headers=headers)
	text = json.loads(response.text)
	companyList = text['system_DiscoverAlbumVO']['companyList']
	print(len(companyList))

	if companyList:
		for company_obj in companyList:
			try:

				company_a = company_obj['company']
				if company_a:
					com_id = company_a.get('id', '')
					code = company_a.get('code', '')
					item_name = company_a.get('name', '')
					com_fullName = company_a.get('fullName', '')
					com_website = company_a.get('website', '')
					com_description = company_a.get('description', '')
					com_brief = company_a.get('brief', '')
					# item_round = company_a.get('round', '')  # todo
					# com_companyStatus = company_a.get('companyStatus', '')
					com_locationId_num = company_a.get('locationId', 0)  # todo
					com_locationId = get_location(com_locationId_num)

					com_address = company_a.get('address', '')

					com_establishDate_num = company_a.get('establishDate', 0)  # todo
					com_establishDate = fmat_stamp(com_establishDate_num)

					com_logo_unhan = company_a.get('logo', '')  # todo
					com_logo = handle_logo(com_logo_unhan)

					com_createTime_num = company_a.get('createTime', 0)  # todo
					com_createTime = fmat_stamp(com_createTime_num)

					com_modifyTime_num = company_a.get('modifyTime', 0)  # todo
					com_modifyTime = fmat_stamp(com_modifyTime_num)

					com_corporateId = company_a.get('corporateId', '')

				tags = company_obj['tags']
				tag_list = []
				if tags:
					for tag in tags:
						com_tag_name = tag.get('name', '')
						tag_list.append(com_tag_name)
				tags = str(tag_list)

				# sql = """update xiniu_com set com_id=%s, code=%s, item_name=%s, com_fullName=%s, com_website=%s, com_description=%s, com_brief=%s, com_locationId=%s, com_address=%s, com_establishDate=%s, com_logo=%s, com_createTime=%s, com_modifyTime=%s, com_corporateId=%s, tags=%s"""
				sql = """replace into xiniu_com (com_id, code, item_name, com_fullName, com_website, com_description, com_brief, com_locationId, com_address, com_establishDate, com_logo, com_createTime, com_modifyTime, com_corporateId, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
				args = (com_id, code, item_name, com_fullName, com_website, com_description, com_brief, com_locationId,
				        com_address, com_establishDate, com_logo, com_createTime, com_modifyTime, com_corporateId, tags)
				cursor.execute(sql, args)
				mysql.commit()
				print(com_id)

				fundings = company_obj['fundings']
				if fundings:
					for funding_obj in fundings:
						try:
							funding = funding_obj.get('funding', '')

							fund_id = funding.get('id', '')
							fund_round_num = funding.get('round', 0)  # todo
							fund_round = get_round(fund_round_num)

							fund_currency = get_currency(funding.get('currency', 0))  # todo

							fund_investment = funding.get('investment', '')
							fund_fundingDate = fmat_stamp(funding.get('fundingDate', 0))  # todo

							fund_modifyTime = fmat_stamp(funding.get('modifyTime', 0))  # todo

							fund_investorsRaw = funding.get('investorsRaw', '')
							fund_investors = funding.get('investors', '')
							fund_newsId = handle_logo(funding.get('newsId', ''))  # todo

							fund_publishDate = fmat_stamp(funding.get('publishDate', 0))  # todo

							fund_corporateId = funding.get('corporateId', '')
							# sql = """update xiniu_fund set fund_id=%s, fund_round=%s, fund_currency=%s, fund_investment=%s, fund_fundingDate=%s, fund_modifyTime=%s, fund_investorsRaw=%s, fund_investors=%s, fund_newsId=%s, fund_publishDate=%s, fund_corporateId=%s"""
							sql = """replace into xiniu_fund (fund_id, fund_round, fund_currency, fund_investment, fund_fundingDate, fund_modifyTime, fund_investorsRaw, fund_investors, fund_newsId, fund_publishDate, fund_corporateId, com_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
							args = (
							fund_id, fund_round, fund_currency, fund_investment, fund_fundingDate, fund_modifyTime,
							fund_investorsRaw, fund_investors, fund_newsId, fund_publishDate, fund_corporateId, com_id)
							cursor.execute(sql, args)
							mysql.commit()
							print(fund_id)

							investors = funding_obj.get('investors', '')
							if investors:
								for investor_obj in investors:
									try:
										inv_id = investor_obj.get('id', '')
										inv_name = investor_obj.get('name', '')
										inv_website = investor_obj.get('website', '')
										inv_description = investor_obj.get('description', '')
										inv_logo = handle_logo(investor_obj.get('logo', ''))  # todo
										inv_stage = investor_obj.get('stage', '')
										inv_field = investor_obj.get('field', '')
										# 这里是 公司类型
										# inv_type = investor_obj.get('type', '')  # todo
										inv_createTime = fmat_stamp(investor_obj.get('createTime', 0))  # todo
										inv_modifyTime = fmat_stamp(investor_obj.get('modifyTime', 0))  # todo
										inv_establishDate = fmat_stamp(investor_obj.get('establishDate', 0))  # todo
										inv_locationId = get_location(investor_obj.get('locationId', 0))  # todo
										inv_fundingCntFrom2017 = investor_obj.get('fundingCntFrom2017', 0)
										# sql = """update xiniu_inve set inv_id=%s, inv_name=%s, inv_website=%s, inv_description=%s, inv_logo=%s, inv_stage=%s, inv_field=%s, inv_createTime=%s, inv_modifyTime=%s, inv_establishDate=%s, inv_locationId=%s, inv_fundingCntFrom2017=%s"""
										sql = """replace into xiniu_inve (inv_id, inv_name, inv_website, inv_description, inv_logo, inv_stage, inv_field, inv_createTime, inv_modifyTime, inv_establishDate, inv_locationId, inv_fundingCntFrom2017, fund_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
										args = (
										inv_id, inv_name, inv_website, inv_description, inv_logo, inv_stage, inv_field,
										inv_createTime, inv_modifyTime, inv_establishDate, inv_locationId,
										inv_fundingCntFrom2017, fund_id)
										cursor.execute(sql, args)
										mysql.commit()
										print(inv_id)
									except:
										print_exc()
										continue
						except:
							print_exc()
							continue
			except:
				print_exc()
				continue


def get_round(num):
	roundSelect = [{"value": 0, "name": "融资未知"}, {"value": 1e3, "name": "未融资"}, {"value": 1010, "name": "种子轮"},
	               {"value": 1011, "name": "天使轮"}, {"value": 1020, "name": "Pre-A轮"}, {"value": 1030, "name": "A轮"},
	               {"value": 1031, "name": "A+轮"}, {"value": 1040, "name": "B轮"}, {"value": 1041, "name": "B+轮"},
	               {"value": 1050, "name": "C轮"}, {"value": 1051, "name": "C+轮"}, {"value": 1060, "name": "D轮"},
	               {"value": 1070, "name": "E轮"}, {"value": 1080, "name": "F轮"}, {"value": 1090, "name": "后期阶段"},
	               {"value": 1100, "name": "Pre-IPO"}, {"value": 1105, "name": "新三板"}, {"value": 1106, "name": "新三板定增"},
	               {"value": 1110, "name": "IPO"}, {"value": 1120, "name": "被收购"}, {"value": 1130, "name": "战略投资"},
	               {"value": 1140, "name": "私有化"}, {"value": 1150, "name": "债权融资"}, {"value": 1160, "name": "股权转让"}]
	round_dict = {a['value']: a['name'] for a in roundSelect}

	return round_dict[num] if num in round_dict.keys() else "融资未知"


def get_location(num):
	locationUseful = [{"name": "北京", "value": 1}, {"name": "上海", "value": 2}, {"name": "深圳", "value": 63},
	                  {"name": "杭州", "value": 360}, {"name": "广州", "value": 52}, {"name": "成都", "value": 296},
	                  {"name": "南京", "value": 185}, {"name": "武汉", "value": 146}, {"name": "未知", "value": 0}]
	local_dict = {a['value']: a['name'] for a in locationUseful}
	return local_dict[num] if num in local_dict.keys() else "未知"


def fmat_stamp(t):
	ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t / 1000)) if t else time.strftime("%Y-%m-%d %H:%M:%S",
	                                                                                          time.localtime(0 / 1000))
	return ti


def handle_logo(logo):
	com_logo = urljoin(base_url, logo) if logo else ''
	return com_logo


def get_currency(num):
	currencySelect = [{"value": 0, "name": "请选择货币"}, {"value": 3020, "name": "人民币"}, {"value": 3010, "name": "美元"},
	                  {"value": 3040, "name": "欧元"}, {"value": 3050, "name": "英镑"}, {"value": 3060, "name": "日元"},
	                  {"value": 3070, "name": "港币"}, {"value": 3030, "name": "新加坡元"}, {"value": 3080, "name": "澳元"}]
	currency_dict = {a['value']: a['name'] for a in currencySelect}
	return currency_dict[num] if num in currency_dict.keys() else "请选择货币"


if __name__ == '__main__':
	tstamp = int(time.time()) * 1000
	# for n in range(1):
	# 	print(n)
	# 	try:
	# 		json_loop(tstamp, 50, 'true')
	# 	except:
	# 		print_exc()
	# 		continue
	# 	tstamp -= 86400 * 1000 * 10


	try:
		json_loop(tstamp, 100, 'false')
		json_loop(tstamp, 100, 'true')
		print('done')
	except:
		print_exc()
