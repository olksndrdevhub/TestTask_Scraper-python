import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
import time
from pprint import pprint
from datetime import datetime, date


from ..selenium_driver import DocSearch, SITE_ADDRESS


searcher = DocSearch()

class BaseSpider(scrapy.spiders.Spider):
    name = 'dataspider'
    start_urls = (SITE_ADDRESS,)

class DataSpider(BaseSpider):
    
    def parse(self, response):    
        searcher.search()
        pages_quantity = searcher.pages_counter()
        for page in range(2, int(pages_quantity)+2):
            scrapy_selector = Selector(text=searcher.browser.page_source)
            rows = scrapy_selector.css('tr.gridRow')
            rowsalt = scrapy_selector.css('tr.gridAltRow')
            for row in rows:
                parsed_description = row.css('td:nth-child(8) > span::text').get()
                splited_description = parsed_description.split(' ')
                street_address = splited_description[-4]+' '+splited_description[-3]
                date_parsed = row.css('td:nth-child(2)::text').get()
                date_splited = date_parsed.split('/')
                date_info = date(year=int(date_splited[-1]), month=int(date_splited[-3]), day=int(date_splited[-2]))
                date_info = date_info.strftime('"%d/%m/%Y"')
                price = 'None'
                state = 'None'
                zip_code = 'None'
                for item in splited_description:
                    description = parsed_description
                    if '$' in item:
                        price = float(item[1:])
                        parsed_description = parsed_description.split(',')
                        description = parsed_description[0]
                        li = description.split(' ')
                        li_reversed = reversed(li)
                        try:
                            for item in li_reversed:
                                if item.isdigit():
                                    index = li.index(item)
                                    description = ' '.join(map(str, li[:int(index)]))
                                    street_address = ' '.join(map(str, li[int(index):]))
                                    break
                                elif '-' in item:
                                    index = li.index(item)
                                    description = ' '.join(map(str, li[:int(index)+1]))
                                    street_address = ' '.join(map(str, li[int(index)+1:]))
                                    break
                                    
                        except:
                            print('smt error')

                    else:
                        splited_description_reversed = reversed(splited_description)
                        try:
                            for item in splited_description_reversed:
                                if item.isdigit():
                                    index = splited_description.index(item)
                                    description = ' '.join(map(str, splited_description[:int(index)]))
                                    street_address = ' '.join(map(str, splited_description[int(index):]))
                                    break
                                elif '-' in item:
                                    index = splited_description.index(item)
                                    description = ' '.join(map(str, splited_description[:int(index)+1]))
                                    street_address = ' '.join(map(str, splited_description[int(index)+1:]))
                                    break
                                    
                        except:
                            print('smt error')

                yield pprint({
                    'page': page-1,
                    'row': 'row',
                    'date': date_info,
                    'type': row.css('td:nth-child(3)::text').get(),
                    'book': row.css('td:nth-child(4)::text').get(),
                    'page_num': row.css('td:nth-child(5)::text').get(),
                    'doc_num': row.css('td:nth-child(6)::text').get(),
                    'city': row.css('td:nth-child(7)::text').get(),
                    'description': description,
                    'cost': price,
                    'street_address': street_address,
                    'state': state,
                    'zip': zip_code,
                })
            for rowalt in rowsalt:
                parsed_description = rowalt.css('td:nth-child(8) > span::text').get()
                splited_description = parsed_description.split(' ')
                street_address = splited_description[-4]+' '+splited_description[-3]
                date_parsed = row.css('td:nth-child(2)::text').get()
                date_splited = date_parsed.split('/')
                date_info = date(year=int(date_splited[-1]), month=int(date_splited[-3]), day=int(date_splited[-2]))
                date_info = date_info.strftime('"%d/%m/%Y"')
                price = 'None'
                state = 'None'
                zip_code = 'None'
                for item in splited_description:
                    description = parsed_description
                    if '$' in item:
                        price = float(item[1:])
                        parsed_description = parsed_description.split(',')
                        description = parsed_description[0]
                        li = description.split(' ')
                        li_reversed = reversed(li)
                        try:
                            for item in li_reversed:
                                if item.isdigit():
                                    index = li.index(item)
                                    description = ' '.join(map(str, li[:int(index)]))
                                    street_address = ' '.join(map(str, li[int(index):]))
                                    break
                                elif '-' in item:
                                    index = li.index(item)
                                    description = ' '.join(map(str, li[:int(index)+1]))
                                    street_address = ' '.join(map(str, li[int(index)+1:]))
                                    break
                        except:
                            print('smt error')
                    else:
                        splited_description_reversed = reversed(splited_description)
                        try:
                            for item in splited_description_reversed:
                                if item.isdigit():
                                    index = splited_description.index(item)
                                    description = ' '.join(map(str, splited_description[:int(index)]))
                                    street_address = ' '.join(map(str, splited_description[int(index):]))
                                    break
                                elif '-' in item:
                                    index = splited_description.index(item)
                                    description = ' '.join(map(str, splited_description[:int(index)+1]))
                                    street_address = ' '.join(map(str, splited_description[int(index)+1:]))
                                    break
                                    
                        except:
                            print('smt error')   

                yield pprint({
                    'page': page-1,
                    'row': 'rowalt',
                    'date': date_info,
                    'type': rowalt.css('td:nth-child(3)::text').get(),
                    'book': rowalt.css('td:nth-child(4)::text').get(),
                    'page_num': rowalt.css('td:nth-child(5)::text').get(),
                    'doc_num': rowalt.css('td:nth-child(6)::text').get(),
                    'city': rowalt.css('td:nth-child(7)::text').get(),
                    'description': description,
                    'cost': price,
                    'street_address': street_address,
                    'state': state,
                    'zip': zip_code,
                })
            
            searcher.next_page(page)
            
            
        time.sleep(5)
        searcher.browser_close()