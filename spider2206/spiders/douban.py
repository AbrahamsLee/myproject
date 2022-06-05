import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from spider2206.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['https://movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def start_requests(self):
        for page in range(20):
            yield Request(
                url=f'https://movie.douban.com/top250?start={page * 25}&filter=',
                # meta={'proxy':''} #代理
                # callback= #回调函数（新的解析数据的函数与parse一样的功能）
                # cb_kwargs= #回调参数（拼接的数据）
            )

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            movie_item = MovieItem()
            movie_item['title'] = list_item.css('span.title::text').extract_first()
            movie_item['rank'] = list_item.css('span.rating_num::text').extract_first()
            movie_item['subject'] = list_item.css('span.inq::text').extract_first()
            yield movie_item
        # 解析url
        # href_list = sel.css(' div.paginator > a::attr(href)')
        # for href in href_list:
        #     url = response.urljoin(href.extract())
        #     yield Request(url=url)
