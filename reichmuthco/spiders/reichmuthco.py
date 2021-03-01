import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from reichmuthco.items import Article


class ReichmuthcoSpider(scrapy.Spider):
    name = 'reichmuthco'
    start_urls = ['https://www.reichmuthco.ch/unsere-meinung/']

    def parse(self, response):
        links = response.xpath('//h2/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//date[@class="post-tease__date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="single-post__content grid-x grid-margin-x"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
