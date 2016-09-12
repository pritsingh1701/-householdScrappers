# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem
from scrapy.http import FormRequest

class SamsonAgencySpider(scrapy.Spider):
	name = "samson_agency"
	start_urls = ['http://www.samson.agency/search_result.php/']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()
		


	def declare_xpath(self):
		self._list_of_posts = "//div[@class='col-md-3 col-sm-6 col-xs-12 products_list']//div[@class='img']/a/@href"
		self._title_xpath = "//div[@id='single_tabs']/h3/text()"
		self._description_xpath = "//div[@class='row welcome_cont prop_description']/p//text()"
		self._prize_xpath = "//div[@id='single_tabs']/span/text()"
		self._location_xpath = "//div[@id='single_tabs']/h3/text()"

	def parse(self, response):
		frmdata = {
				"property_type":"1",
				"bedroom":"1+",
				"pricemin" : "0",
				"pricemax":"0",
				"offer" :'',
				"form_from":"buy",
				"submit":"Search Now"
				}
		url = "http://www.samson.agency/search_result.php"
		yield FormRequest(url, callback=self.parse_two, formdata=frmdata)
	

	def parse_two(self,response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)



	def parse_info(self,response):

		Typo = 'Buy'

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_type = prize.replace("Price","").split("-")[1]

		prize = prize.replace("Price","").split("-")[0]


		item = DarkmatterItem()

		item['url']                 = response.url
		item['title']               = title
		item['description']         = description
		item['location_address']    = location
		item['zipCode']             = ''
		item['Type']                = Typo                       
		item['ObjectType']          = ''
		item['Price']               = prize
		item['PriceType']           = prize_type
		item['Rooms']               = ''
		item['Bathrooms']           = ''
		item['Bedrooms']            = ''
		item['Square']              = ''
		yield item



	def listToStr(self,MyLst):
		_dumm = ""
		for i in MyLst:_dumm = "%s %s"%(_dumm,i)
		return _dumm


	def parseText(self, str):
		soup = BeautifulSoup(str, 'html.parser')
		return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()

	def cleanText(self,text):
		soup = BeautifulSoup(text,'html.parser')
		text = soup.get_text();
		text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
		return text 

