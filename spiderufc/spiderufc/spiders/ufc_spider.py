import scrapy
from scrapy.loader import ItemLoader

from spiderufc.items import SpiderufcItem

class UfcSpider(scrapy.Spider):
    name =  'ufc'

    def start_requests(self):
        urls = ['https://www.ufc.com.br/athlete/deiveson-figueiredo']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        loader = ItemLoader(item=SpiderufcItem(), response=response)

        loader.add_value('nickname', response.xpath('normalize-space(.//*[@class="field field-name-nickname"])').extract_first())
        loader.add_value('real_name', response.xpath('normalize-space(.//*[@class="field field-name-name"])').extract_first())
        loader.add_value('category_position', response.xpath('normalize-space(.//*[@class="c-hero__headline-suffix"])').extract_first())
        loader.add_value('win_streak', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[4]/div/section/ul[1]/li[1]/div/div/div[1]/text()').extract_first())
        loader.add_value('win_ko', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[4]/div/section/ul[1]/li[2]/div/div/div[1]/text()').extract_first())
        loader.add_value('win_subm', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[4]/div/section/ul[1]/li[3]/div/div/div[1]/text()').extract_first())
        loader.add_value('strike_prec', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[5]/div/section/div[1]/div/div/div[1]/div/svg/text/text()').extract_first())
        loader.add_value('grap_prec', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[5]/div/section/div[2]/div/div/div[1]/div/svg/text/text()').extract_first())

        yield loader.load_item()