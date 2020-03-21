# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from spider.book.items import BookItem, CommentItem

class DoubanSpider(Spider):
    name = 'test'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/']
    
    def parse(self, response):
        book_item = BookItem({
            'id': '1770782',
            'name': '追风筝的人',
            'author_ids': ['008393'],
            'tags': ['人性', '小说'],
            'publisher': '上海人民出版社',
            'price': 29.0,
            'isbn': '9787208061644',
            'page_number': 363,
            'introduction': '12岁的阿富汗富家少爷阿米尔与仆人哈桑情同手足。然而，在一场风筝比赛后，发生了一件悲惨不堪的事，阿米尔为自己的懦弱感到自责和痛苦，逼走了哈桑，不久，自己也跟随父亲逃往美国。成年后的阿米尔始终无法原谅自己当年对哈桑的背叛。为了赎罪，阿米尔再度踏上暌违二十多年的故乡，希望能为不幸的好友尽最后一点心力，却发现一个惊天谎言，儿时的噩梦再度重演，阿米尔该如何抉择？故事如此残忍而又美丽，作者以温暖细腻的笔法勾勒人性的本质与救赎，读来令人荡气回肠。'
        })
        comment_item = CommentItem({
            'id': '1036294715',
            'content': '两年前，我在美国上一门英语课。坐在我旁边的男孩就来自阿富汗。当他用英语说出这个名字的时候，我们都以为他穿过重重战火和历史的沉疴而来，身上闪耀着神圣的荣光。而他，只是一个普通的阿富汗男孩，好像天空下奔跑着追风筝的人。',
            'book_id': '17707842'
        })
        yield comment_item
        yield book_item
