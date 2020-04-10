import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
import time
import re

from ..selenium_driver import DocSearch, SITE_ADDRESS


searcher = DocSearch()

class DataSpider(scrapy.Spider):
    name = 'dataspider'
    start_urls = (SITE_ADDRESS,)

    def parse(self, response):
        
        searcher.search()
        pages_quantity = searcher.pages_counter()
        for page in range(2, int(pages_quantity)+2):
            scrapy_selector = Selector(text=searcher.browser.page_source)
            rows = scrapy_selector.css('tr.gridRow')
            rowsalt = scrapy_selector.css('tr.gridAltRow')
            for row in rows:
                description = row.css('td:nth-child(8) > span::text').get()
                print(description)
                parsed_description = description.split(' ')
                street_address = parsed_description[-4]+' '+parsed_description[-3]
                price = None
                for item in parsed_description:
                    if '$' in item:
                        price = item
                        description = description.split(',')[0]
                        # street_address = parsed_description[-3]+parsed_description[-4]
                print(parsed_description)
                print(len(parsed_description))
                yield {
                    'page': page-1,
                    'row': 'row',
                    'date': row.css('td:nth-child(2)::text').get(),
                    'type': row.css('td:nth-child(3)::text').get(),
                    'book': row.css('td:nth-child(4)::text').get(),
                    'page_num': row.css('td:nth-child(5)::text').get(),
                    'doc_num': row.css('td:nth-child(6)::text').get(),
                    'city': row.css('td:nth-child(7)::text').get(),
                    'description': description,
                    'cost': price,
                    'street_address': street_address,
                    'state': row.css('td:nth-child(2)::text').get(),
                    'zip': row.css('td:nth-child(2)::text').get(),
                }
            for rowalt in rowsalt:
                description = rowalt.css('td:nth-child(8) > span::text').get()
                print(description)
                parsed_description = description.split(' ')
                street_address = parsed_description[-4]+' '+parsed_description[-3]
                price = None
                for item in parsed_description:
                    if '$' in item:
                        price = item
                        description = description.split(',')[0]
                        # street_address =parsed_description[-3]+parsed_description[-4]
                print(parsed_description)
                print(len(parsed_description))
                yield {
                    'page': page-1,
                    'row': 'rowalt',
                    'date': rowalt.css('td:nth-child(2)::text').get(),
                    'type': rowalt.css('td:nth-child(3)::text').get(),
                    'book': rowalt.css('td:nth-child(4)::text').get(),
                    'page_num': rowalt.css('td:nth-child(5)::text').get(),
                    'doc_num': rowalt.css('td:nth-child(6)::text').get(),
                    'city': rowalt.css('td:nth-child(7)::text').get(),
                    'description': description,
                    'cost': price,
                    'street_address': street_address,
                    'state': rowalt.css('td:nth-child(2)::text').get(),
                    'zip': rowalt.css('td:nth-child(2)::text').get(),
                }
            searcher.next_page(page)

        time.sleep(5)
        searcher.browser_close()
        # //*[@id="ctl00_cphMainContent_gvSearchResults"]/tbody/tr[21]/td[1]
        #ctl00_cphMainContent_gvSearchResults > tbody > tr:nth-child(3) > td:nth-child(1)
        #ctl00_cphMainContent_gvSearchResults > tbody > tr:nth-child(5) > td:nth-child(1)
        #ctl00_cphMainContent_gvSearchResults > tbody > tr:nth-child(6) > td:nth-child(1)#ctl00_cphMainContent_gvSearchResults > tbody > tr:nth-child(6)
        #ctl00_cphMainContent_gvSearchResults_ctl06_lblDescription