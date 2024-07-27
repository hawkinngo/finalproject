# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# CategoryItem, ProductItem, ProductReview

class CategoryItem(scrapy.Item):
    title = scrapy.Field()
    icon = scrapy.Field()
    link = scrapy.Field()
    category_id = scrapy.Field()


class ProductItem(scrapy.Item):
    id = scrapy.Field()
    spid = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    brand_id = scrapy.Field()
    brand_name = scrapy.Field()
    original_price = scrapy.Field()
    list_price = scrapy.Field()
    discount = scrapy.Field()
    quantity_sold = scrapy.Field()
    rating_average = scrapy.Field()
    review_count = scrapy.Field()
    description = scrapy.Field()
    short_description = scrapy.Field()
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    current_seller = scrapy.Field()
    other_sellers = scrapy.Field()
    specifications = scrapy.Field()

class ProductReview(scrapy.Item):
    review_id = scrapy.Field()
    comment_id = scrapy.Field()
    product_id = scrapy.Field()
    spid = scrapy.Field()
    rating = scrapy.Field()
    comment = scrapy.Field()
    status = scrapy.Field()
    seller_id = scrapy.Field()