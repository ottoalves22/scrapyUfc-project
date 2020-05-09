import scrapy
from scrapy.loader import ItemLoader
from spiderufc.items import SpiderFighterItem
from mongoengine import connect
from models import Fighter
from pathlib import Path

sett = str(Path(__file__).parent.parent) + '/settings.txt'
f = open(sett, 'r')

MONGO_URI = f.readline()
print(MONGO_URI)
connect('ufcData', host=MONGO_URI)

class UfcSpider(scrapy.Spider):
    name =  'ufc'
    #allowed_domains = ["espn.com", "ufc.com"]
    fightersUrls = []
    ufc = 'https://www.ufc.com.br'

    def start_requests(self):
        urls = ['https://www.ufc.com.br/rankings']
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


    def parseFighterInfo(self, response):

        loaderFighter = ItemLoader(item=SpiderFighterItem(), response=response)

        loaderFighter.add_value('nickname', response.xpath('normalize-space(.//*[@class="field field-name-nickname"])').extract_first())
        loaderFighter.add_value('real_name', response.xpath('normalize-space(.//*[@class="field field-name-name"])').extract_first())
        loaderFighter.add_value('category_position', response.xpath('normalize-space(.//*[@class="c-hero__headline-suffix"])').extract_first())
        loaderFighter.add_value('strike_prec', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[5]/div/section/div[1]/div/div/div[1]/div/svg/text/text()').extract_first())
        loaderFighter.add_value('grap_prec', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[5]/div/section/div[2]/div/div/div[1]/div/svg/text/text()').extract_first())
        #bio = response.xpath('//*[@class="c-bio__info-details"]')
        loaderFighter.add_value('height', response.xpath('.//*[@class="c-bio__row--3col"][1]/div[@class="c-bio__field"][2]/div[2]/text()').extract_first())
        loaderFighter.add_value('armWingspan', response.xpath('.//*[@class="c-bio__row--3col"][2]/div[@class="c-bio__field"][2]/div[2]/text()').extract_first())
        loaderFighter.add_value('legWingspan', response.xpath('.//*[@class="c-bio__row--3col"][2]/div[@class="c-bio__field"][3]/div[2]/text()').extract_first())
        yield loaderFighter.load_item()

    def mongoInsert(self, nickname, realName, cat_pos, strikePrc, grapPrc, height, arms, legs):
        fighter = Fighter()
        fighter.nickname = nickname
        fighter.real_name = realName
        fighter.category_position = cat_pos
        fighter.height = float(height)
        fighter.armWingspan = float(arms)
        fighter.legWingspan = float(legs)
        fighter.strike_prec = int(strikePrc.replace('%', ''))
        fighter.grap_prec = int(grapPrc.replace('%', ''))
        #todo tratar precisoes pra number