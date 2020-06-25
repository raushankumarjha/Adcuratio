'''scrape Hackernews'''
import pymongo
import scrapy

mongo_client = pymongo.MongoClient("mongodb://localhost:26745/")
hn_data = mongo_client['hn_database']

headings = hn_data["headings"]
metadata = hn_data["metadata"]

class HNSpider(scrapy.Spider):
    name = 'hackernews-spider'
    start_urls = ['https://news.ycombinator.com']

    def parse(self, response):
        page_content = []
        item_list = response.xpath(
            '//table[@class="itemlist"]//tr[not(@class) or contains(@class, "athing")]')
        ele_for_next = item_list[-1]
        item_list = item_list[:-1]
        i = 0
        while i < len(item_list):
            data = {}
            data['title'] = item_list[i].xpath(
                './/a[@class="storylink"]/text()')[0].get()
            data['url'] = item_list[i].xpath(
                './/a[@class="storylink"]/@href')[0].get()
            data['id'] = int(item_list[i].xpath('./@id')[0].get())
            page_content.append(data)
            yield data
            i += 2

# Mongodb
        headings_data = [
            {'url': data['url'], 'title': data['title']}
            for data in page_content
            ]
        metadata_items = [
            {
                'url': data['url'], '_id': data['id'],
                'image_url': data['image_url'], 'votes': data['votes'],
                'author': data['author']
            } for data in page_content]
