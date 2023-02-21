import scrapy
import json
from scrapy import Item, Field



class OfferItem(Item):
    title = Field()
    image_url = Field()


class SrealitySpider(scrapy.Spider):
    name = "sreality"
    allowed_domains = ["sreality.cz"]
    start_urls = [f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=500"]
    max_offers = 500

    def parse(self, response):
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract the offer data
        for i, offer in enumerate(data["_embedded"]["estates"]):
            if i >= self.max_offers:
                break

            # Extract the title
            title = offer["name"]

            # Extract the first image
            image_url = offer["_links"]["images"][0]["href"]

            item = OfferItem()
            item["title"] = title
            item["image_url"] = image_url

            yield item