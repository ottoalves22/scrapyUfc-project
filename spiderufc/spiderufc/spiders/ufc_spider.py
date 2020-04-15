import scrapy
from scrapy.loader import ItemLoader
from spiderufc.items import SpiderFighterItem
from mongoengine import connect
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
connect('ufcData', host=MONGO_URI)

class UfcSpider(scrapy.Spider):
    name =  'ufc'
    allowed_domains = ["espn.com", "ufc.com"]
    fightersUrls = []
    ufc = 'https://www.ufc.com'

    def start_requests(self):
        urls = ['https://www.ufc.com/rankings']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseCategoryList)

    def parseCategoryList(self, response):
        #TODO usar mais de um parse
        #essa tabela é a tabela da categoria, os seletores pra baixo são relativos desta
        table = response.xpath('/html/body/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div[11]/div[2]/table')
        category = table.xpath('.//tbody//tr')
        championUrl = table.xpath('.//caption/div/div[1]/h5/div/div/div/a/@href').extract_first()
        self.fightersUrls.append(self.ufc + str(championUrl))

        for f in category:
            fgt = self.ufc + f.xpath('td//a/@href').extract_first()
            self.fightersUrls.append(fgt)

        for fighter in self.fightersUrls:
            yield scrapy.Request(url=fighter, callback=self.parseFighterInfo)

        print(self.fightersUrls)


    def parseFighterInfo(self, response):

        loaderFighter = ItemLoader(item=SpiderFighterItem(), response=response)

        loaderFighter.add_value('nickname', response.xpath('normalize-space(.//*[@class="field field-name-nickname"])').extract_first())
        loaderFighter.add_value('real_name', response.xpath('normalize-space(.//*[@class="field field-name-name"])').extract_first())
        loaderFighter.add_value('category_position', response.xpath('normalize-space(.//*[@class="c-hero__headline-suffix"])').extract_first())
        loaderFighter.add_value('strike_prec', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[5]/div/section/div[1]/div/div/div[1]/div/svg/text/text()').extract_first())
        loaderFighter.add_value('grap_prec', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[5]/div/section/div[2]/div/div/div[1]/div/svg/text/text()').extract_first())
        bio = response.xpath('//*[@class="c-bio__info-details"]')
        loaderFighter.add_value('height', bio.xpath('.//div[3]/div[1]/div[1]/text()').extract_first())
        loaderFighter.add_value('armWingspan', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[8]/div/div/div/div[3]/div[1]/div[4]/div[2]/div[2]/text()').extract_first())
        loaderFighter.add_value('legWingspan', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[8]/div/div/div/div[3]/div[1]/div[4]/div[3]/div[2]/text()').extract_first())
        yield loaderFighter.load_item()
