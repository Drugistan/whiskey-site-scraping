import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def clean_price(symbol):
    if "$" in symbol:
        return symbol.split("$")[-1]


def clean_product_title(title):
    string_title = title.replace('\n', '')
    string_title = string_title.replace('\r', '')
    string_title = string_title.replace('\"', '')
    return string_title


class WiskeyItem(scrapy.Item):
    product_title = scrapy.Field(
        input_processor=MapCompose(clean_product_title),

        output_processor=TakeFirst()
    )
    product_price = scrapy.Field(
        input_processor=MapCompose(clean_price),
        output_processor=TakeFirst()

    )

    product_brand = scrapy.Field(
        output_processor=TakeFirst()
    )
    product_description = scrapy.Field(
        input_processor=MapCompose(clean_product_title),
        output_processor=TakeFirst()
    )
