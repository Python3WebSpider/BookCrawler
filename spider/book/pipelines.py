# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.db import IntegrityError
import logging
from merry import Merry
from spider.book.items import BookItem, CommentItem
from app.models import Book, Comment

merry = Merry()
logger = logging.getLogger(__name__)

class PgSQLPipeline():
    """
    save data to postgresql
    """
    
    @merry._try
    def process_item(self, item, spider):
        merry.g.item = item
        logger.debug('Process item type %s', type(item))
        if isinstance(item, BookItem):
            item.instance.save()
            logger.info('Saved book %s', item.instance)
        
        if isinstance(item, CommentItem):
            book_id = item.get('book_id')
            book, created = Book.objects.get_or_create(id=book_id)
            logger.info('Created book %s' if created else 'Book %s exists', book)
            item.instance.book = book
            item.instance.save()
            logger.info('Saved book %s', item.instance)
        
        return item
    
    @merry._except(IntegrityError)
    def process_integrity_error(self, e):
        item = merry.g.item
        logger.info('《%s》of %s already exists', item.get('title'), item.get('website'))
