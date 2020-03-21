# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from app.models import Book, Comment
from scrapy.item import Field

class BookItem(DjangoItem):
    django_model = Book
    author_ids = Field()

class CommentItem(DjangoItem):
    django_model = Comment
    book_id = Field()