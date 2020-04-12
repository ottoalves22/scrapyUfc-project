import scrapy
from scrapy.loader import ItemLoader

from spiderufc.items import SpiderFighterItem

class UfcSpider(scrapy.Spider):
    name =  'ufc'
    allowed_domains = ["espn.com"]
    fightersUrls = []
    ufc = 'https://www.ufc.com.br'

    def start_requests(self):
        urls = ['https://www.ufc.com.br/rankings']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseCategoryList)

    def parseCategoryList(self, response):
        #TODO usar mais de um parse
        #pegar caregoria, iterar pela categoria pegando urls de lutadores, indice 0 sendo o campeao na lista Fighters
        category = response.xpath('/html/body/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div[11]/div[2]/table//tbody//tr')
        championUrl =  self.ufc + response.xpath('/html/body/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div[7]/div[2]/table/caption/div/div[1]/h5/div/div/div/a/@href').extract_first()
        self.fightersUrls.append(championUrl)

        #pega a tabela de lutadoras peso-palha:
        #fightersList = response.xpath('/html/body/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div[11]/div[2]/table//tr')

        for f in category:
            fgt = self.ufc + f.xpath('td//a/@href').extract_first()
            self.fightersUrls.append(fgt)

        print(self.fightersUrls)

        '''
        loaderFighter = ItemLoader(item=SpiderFighterItem(), response=response)

        loaderFighter.add_value('nickname', response.xpath('normalize-space(.//*[@class="field field-name-nickname"])').extract_first())
        loaderFighter.add_value('real_name', response.xpath('normalize-space(.//*[@class="field field-name-name"])').extract_first())
        loaderFighter.add_value('category_position', response.xpath('normalize-space(.//*[@class="c-hero__headline-suffix"])').extract_first())
        loaderFighter.add_value('win_streak', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[4]/div/section/ul[1]/li[1]/div/div/div[1]/text()').extract_first())
        loaderFighter.add_value('win_ko', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[4]/div/section/ul[1]/li[2]/div/div/div[1]/text()').extract_first())
        loaderFighter.add_value('win_subm', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[4]/div/section/ul[1]/li[3]/div/div/div[1]/text()').extract_first())
        loaderFighter.add_value('strike_prec', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[5]/div/section/div[1]/div/div/div[1]/div/svg/text/text()').extract_first())
        loaderFighter.add_value('grap_prec', response.xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div[2]/div[5]/div/section/div[2]/div/div/div[1]/div/svg/text/text()').extract_first())

        yield loaderFighter.load_item()
        '''