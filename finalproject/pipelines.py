# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import csv
import os

from scrapy.exceptions import DropItem

from .items import CategoryItem, ProductItem, ProductReview

class MongoPipeline:
    def __init__(self):

        self.client = pymongo.MongoClient(f"mongodb://{os.environ['DBHOST']}:27017/")
        self.db = self.client["tikidb2"]

        pass

    def process_item(self, item, spider):

        if isinstance(item, CategoryItem):
            collection = self.db["tiki_category"]
            try:
                collection.insert_one(dict(item))
                return item
            except Exception as e:
                raise DropItem(f"Error inserting item: {e}")

        if isinstance(item, ProductItem):
            collection = self.db["tiki_product"]
            try:
                collection.insert_one(dict(item))
                return item
            except Exception as e:
                raise DropItem(f"Error inserting item: {e}")
            
        if isinstance(item, ProductReview):
            collection = self.db["tiki_product_review"]
            try:
                collection.insert_one(dict(item))
                return item
            except Exception as e:
                raise DropItem(f"Error inserting item: {e}")

class CSVPipeline:
    def process_item(self, item, spider):
        
        if isinstance(item, CategoryItem):
            with open("csvdb_tiki_category.csv", "a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file, delimiter="|")
                writer.writerow(
                    [
                        item["title"],
                        item["icon"],
                        item["link"],
                        item["category_id"]
                    ]
                )

        if isinstance(item, ProductItem):
            with open("csvdb_tiki_product.csv", "a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file, delimiter="|")
                writer.writerow(
                    [
                        item["id"],
                        item["spid"],
                        item["sku"],
                        item["name"],
                        item["url"],
                        item["brand_name"],
                        item["original_price"],
                        item["list_price"],
                        item["discount"],
                        item["quantity_sold"],
                        item["rating_average"],
                        item["review_count"],
                        item["short_description"],
                        item["description"],
                        item["category_id"],
                        item["category_name"]
                    ]
                )


        if isinstance(item, ProductReview):
            with open("csvdb_tiki_product_review.csv", "a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file, delimiter="|")
                writer.writerow(
                    [
                        item["review_id"],
                        item["comment_id"],
                        item["product_id"],
                        item["spid"],
                        item["rating"],
                        item["comment"],
                        item["status"],
                        item["seller_id"]
                    ]
                )

        return item
