import scrapy

from scrapy.loader import ItemLoader

from ..items import EmiratesislamicaeItem
from itemloaders.processors import TakeFirst


class EmiratesislamicaeSpider(scrapy.Spider):
	name = 'emiratesislamicae'
	start_urls = ['https://www.emiratesislamic.ae/eng/latest-news/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="list-item box"]')
		for post in post_links:
			url = post.xpath('.//h4/a/@href').get()
			date = post.xpath('.//span[@class="date"]/text()').get()
			title = post.xpath('.//h2[@class="title"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, title, date):
		description = response.xpath('//div[@class="col-12 col-md-12"]//text()[normalize-space()]|//div[contains(@class,"detail-bg")]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=EmiratesislamicaeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
