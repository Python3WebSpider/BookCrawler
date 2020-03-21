# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import re
import json
import dateparser
import pytz
from spider.book.items import BookItem, CommentItem

class DoubanSpider(Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']
    tz = pytz.timezone('Asia/Shanghai')
    
    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url, callback=self.parse_list)
        # yield Request(url='https://book.douban.com/subject/30329536/', callback=self.parse_detail)
    
    def parse_list(self, response):
        tags = response.css('.tagCol td a::attr(href)').extract()
        for tag in tags:
            index_url = response.urljoin(tag)
            yield Request(index_url, callback=self.parse_index)
    
    def parse_index(self, response):
        hrefs = response.css('.subject-item h2 a::attr(href)').extract()
        for href in hrefs:
            detail_url = response.urljoin(href)
            yield Request(detail_url, callback=self.parse_detail)
        
        next_href = response.xpath('//a[contains(text(), "后页")]/@href').extract_first()
        next_url = response.urljoin(next_href)
        yield Request(next_url, callback=self.parse_index)
    
    def parse_detail(self, response):
        
        book_name = response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first().strip()
        book_cover = response.css('#mainpic a.nbg::attr(href)').extract_first().strip()
        book_introduction = ''.join(response.xpath(
            '//h2[contains(., "内容简介")]/following-sibling::div[@class="indent"]//span[contains(@class, "hidden")]//div[@class="intro"]//p//text()').extract())
        book_authors = \
            response.xpath(
                '//span[contains(text(), "作者") and @class="pl"]/following-sibling::a//text()').extract()
        book_translators = \
            response.xpath(
                '//span[contains(text(), "译者") and @class="pl"]/following-sibling::a//text()').extract()
        book_publisher = response.xpath(
            '//span[contains(text(), "出版社") and @class="pl"]/following-sibling::text()').extract_first()
        book_publisher = book_publisher.strip() if book_publisher else None
        book_page_number = response.xpath(
            '//span[contains(text(), "页数") and @class="pl"]/following-sibling::text()').extract_first()
        book_page_number = book_page_number.strip() if book_page_number else None
        book_isbn = response.xpath(
            '//span[contains(text(), "ISBN") and @class="pl"]/following-sibling::text()').extract_first()
        book_isbn = book_isbn.strip() if book_isbn else None
        book_published_at = response.xpath(
            '//span[contains(text(), "出版年") and @class="pl"]/following-sibling::text()').extract_first()
        book_published_at = self.tz.localize(dateparser.parse(book_published_at)) if book_published_at else None
        book_price = response.xpath(
            '//span[contains(text(), "定价") and @class="pl"]/following-sibling::text()').extract_first()
        book_price = book_price.strip() if book_price else None
        book_id = re.search('subject/(\d+)', response.url).group(1)
        book_url = response.url
        book_score = response.css('.rating_num::text').extract_first()
        book_score = book_score.strip() if book_score else None
        book_catalog = ''.join(
            response.xpath('//h2[contains(., "目录")]/following-sibling::div[contains(@id, "full")]//text()').extract())
        book_catalog = book_catalog.replace(' (收起)\n', '') if book_catalog else None
        book_tags = response.xpath(
            '//div[contains(@id, "tags-section")]//div[@class="indent"]//span//a//text()').extract()
        book_item = BookItem({
            'id': book_id,
            'name': book_name,
            'publisher': book_publisher,
            'page_number': book_page_number,
            'isbn': book_isbn,
            'published_at': book_published_at,
            'price': book_price,
            'url': book_url,
            'authors': book_authors,
            'translators': book_translators,
            'score': book_score,
            'catalog': book_catalog,
            'cover': book_cover,
            'introduction': book_introduction,
            'tags': book_tags
        })
        yield book_item
        
        for comment_dom in response.css('.comment-item'):
            comment_id = comment_dom.xpath('./@data-cid').extract_first()
            comment_content = comment_dom.xpath('.//span[@class="short"]/text()').extract_first()
            comment_item = CommentItem({
                'id': comment_id,
                'content': comment_content,
                'book_id': book_id
            })
            yield comment_item
