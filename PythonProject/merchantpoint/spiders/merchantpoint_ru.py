import scrapy
from scrapy.spiders import SitemapSpider


class MerchantpointRuSpider(SitemapSpider):
    name = "merchantpoint_ru"
    allowed_domains = ["merchantpoint.ru"]

    sitemap_urls = ["https://merchantpoint.ru/sitemap/brands.xml"]
    sitemap_rules = [
        (r"/brand", "parse_brand"),
    ]

    custom_settings = {
        "ITEM_PIPELINES": {
            "merchantpoint.pipelines.CuCrawlingPipeline": 300,
        },
        "CLOSESPIDER_ITEMCOUNT": 1000,
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "AUTOTHROTTLE_ENABLED": True,
    }

    def parse_brand(self, response: scrapy.http.Response):
        raw_org_description = response.xpath(
            "//div[contains(@class, 'description_brand')]//text()"
        ).getall()
        org_description = " ".join(
            [t.strip() for t in raw_org_description if t.strip()]
        )

        merchant_urls = response.xpath(
            "//table[contains(@class, 'finance-table')]//a/@href"
        ).getall()

        yield from response.follow_all(
            urls=merchant_urls,
            cb_kwargs={"org_description": org_description},
            callback=self.parse_merchant,
        )

    def parse_merchant(self, response: scrapy.http.Response, org_description: str):
        return {
            "merchant_name": response.xpath("//h1/text()").get(),
            "mcc": response.xpath(
                "//section[@id='description']//p/a/text()"
            ).get(),
            "address": response.xpath(
                "//div//p[contains(., 'Адрес')]/text()"
            ).get(),
            "geo_coordinates": response.xpath(
                "//div//p[contains(., 'Гео')]/text()"
            ).get(),
            "org_name": response.xpath(
                "//p/a[contains(@href,'brand')]/text()"
            ).get(),
            "org_description": org_description,
            "source_url": response.url,
        }
