import scrapy
import json

from finalproject.items import ProductItem, ProductReview

class TikiphoneSpider(scrapy.Spider):
    name = "tikiphone"
    allowed_domains = ["api.tiki.vn", "tiki.vn"]
    start_urls = ["https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&category=1789&sort=newest&page=1"]

    url_category = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&category=1789&sort=newest"
    url_product = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=40"
    url_product_detail = "https://tiki.vn/api/v2/products"
    url_product_review = "https://tiki.vn/api/v2/reviews?limit=20&seller_id=1&include=comments,contribute_info,attribute_vote_summary&sort=score|desc,id|desc,stars|all"

    def parse(self, response):
        response_json = json.loads(response.body)
        
        last_page = response_json["paging"]["last_page"]
        product_list = response_json["data"]

        for product_index in range(len(product_list)):
            one_product = product_list[product_index]
                
            product_id = one_product["id"]
            url_product_detail = f"{self.url_product_detail}/{product_id}"

            request_product_detail = scrapy.Request(url = url_product_detail, callback=self.parseProductDetail)
            yield request_product_detail


        for one_page in range(2, last_page+1):
            url_product_map = f"{self.url_category}&page={one_page}"
            
            request = scrapy.Request(url = url_product_map, callback=self.parseProductList)
            yield request

    def parseProductDetail(self, response):
        one_product = json.loads(response.body)
        item = ProductItem()

        item["id"] = one_product["id"]
        item["spid"] = one_product["current_seller"]["product_id"]
        item["sku"]=one_product["sku"]
        item["name"]=one_product["name"]
        item["url"]=one_product["url_key"]
        item["brand_id"] = one_product["brand"]["id"] if 'brand' in one_product else "Unknown"
        item["brand_name"] = one_product["brand"]["name"] if 'brand' in one_product else "Unknown"
        item["original_price"]=one_product["original_price"]
        item["list_price"]=one_product["list_price"]
        item["discount"]=one_product["discount"]
        item["quantity_sold"]=one_product["quantity_sold"]["value"] if 'quantity_sold' in one_product else "Unknown"
        item["rating_average"]=one_product["rating_average"]
        item["review_count"]=one_product["review_count"]
        item["description"]= " ".join(line.strip() for line in one_product["description"].splitlines())
        item["short_description"]=one_product["short_description"]
        item["category_id"]=one_product["categories"]["id"]
        item["category_name"]=one_product["categories"]["name"]
        item["current_seller"]=one_product["current_seller"]
        item["other_sellers"]=one_product["other_sellers"]
        item["specifications"]=one_product["specifications"]
        yield item

        total_review_page = int((item["review_count"] / 20 if item["review_count"] % 20 else int(item["review_count"] / 20) + 1)+1)

        for review_index_page in range(1, total_review_page):
            url_product_map = f"{self.url_product_review}&page={review_index_page}&spid={item["spid"]}&product_id={item["id"]}"
            request_product_review = scrapy.Request(url = url_product_map, callback=self.parseProductReview)
            yield request_product_review

    def parseProductList(self, response):
        response_json = json.loads(response.body)
        product_list = response_json["data"]

        for product_index in range(len(product_list)):
            one_product = product_list[product_index]
                
            product_id = one_product["id"]
            url_product_detail = f"{self.url_product_detail}/{product_id}"

            request_product_detail = scrapy.Request(url = url_product_detail, callback=self.parseProductDetail)
            yield request_product_detail

    def parseProductReview(self, response):
        response_json = json.loads(response.body)
        review_list = response_json["data"]

        for one_review in review_list:
            total_comment = len(one_review["comments"])

            if total_comment == 0: continue

            for one_comment in one_review["comments"]:
                item = ProductReview()
                
                item["review_id"] = one_comment["review_id"]
                item["comment_id"] = one_comment["id"]
                item["product_id"] = one_review["product_id"]
                item["spid"] = one_review["spid"]
                item["rating"] = one_review["rating"]
                item["comment"] = one_comment["content"]
                item["status"] = one_review["status"]
                item["seller_id"] = one_review["seller"]["id"]

                yield item