import scrapy
from itemloaders import ItemLoader

from ..items import WiskeyItem


class WhiskeySpider(scrapy.Spider):
    name = 'whiskey'
    allowed_domains = ['sipwhiskey.com/']
    start_urls = ['http://sipwhiskey.com/']

    def parse(self, response, **kwargs):
        get_url_links_xpath = response.xpath(
            '//div/div[@id="main-nav"]//div[@class="tier-1"]/ul//li//a//@href').getall()
        print(get_url_links_xpath)
        for links in get_url_links_xpath:
            url = response.urljoin("https://sipwhiskey.com/{}".format(links))
            if "login" not in url:
                yield scrapy.Request(
                    url, callback=self.product_links, dont_filter=True
                )

    def product_links(self, response):
        product_links = response.xpath('//a[@class="product-link"]//@href').getall()
        for links in product_links:
            url = response.urljoin("https://sipwhiskey.com/{}".format(links))
            if "login" not in url:
                yield scrapy.Request(
                    url, callback=self.parse_products, dont_filter=True
                )

    def parse_products(self, response):
        item_loader = ItemLoader(item=WiskeyItem(), selector=response)
        item_loader.add_xpath(
            "product_title", "//h1[@class='title']/text()"
        )
        item_loader.add_xpath(
            "product_price", "//span[@class='price theme-money']//text()"
        )

        item_loader.add_xpath(
            "product_brand", "//div[@class='vendor']/a/text()"
        )
        item_loader.add_xpath(
            "product_description", "//div[@class='description user-content']//text()"
        )

        return item_loader.load_item()
