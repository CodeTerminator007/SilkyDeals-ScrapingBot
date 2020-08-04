import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector 

class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://slickdeals.net/computer-deals/",
            wait_time=3,            
            callback=self.parse,
        )

        
    def parse(self, response):
        linkfordeal = 'https://slickdeals.net/'
        deals = response.xpath('//li[@class="fpGridBox grid " or @class="fpGridBox grid altDeal hasPrice"]')
        for deal in deals:
            yield {
                'Name' : deal.xpath('.//div/div/div[1]/div[1]/div/a/text()').get(),
                'Link' : f"{linkfordeal}{deal.xpath('.//div/div/div[1]/div[1]/div/a/@href').get()}",
                'Shop Name' : deal.xpath('.//div/div/div[1]/div[1]/div/span/a/text()').get(),
                'item-Price' : deal.xpath('normalize-space(.//div/div/div[1]/div[2]/div[2]/div/text())').get(),
                'Likes' : deal.xpath('.//div/div/div[2]/div[1]/span/span[2]/text()').get(),
                'Comments' : deal.xpath('.//div/div/div[2]/div[2]/span[2]/text()').get()                
            }
        next_page = response.xpath('//a[@data-role="next-page"]/@href').get()

        if next_page:
            absolute_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(                
                url=absolute_url,
                wait_time=3,
                callback=self.parse

            )
        
        