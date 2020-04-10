import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

SITE_ADDRESS = 'http://www.tauntondeeds.com/Searches/ImageSearch.aspx'

class DocSearch():
    def __init__(self):
        opts = Options()
        opts.headless = True
        self.browser = webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver', options=opts)
        self.browser.get(SITE_ADDRESS)
        time.sleep(4)

    def search(self):
        self.submit_button = self.browser.find_elements_by_id('ctl00_cphMainContent_btnSearchRL')
        self.input_date_start = self.browser.find_elements_by_id('ctl00_cphMainContent_txtRLStartDate_dateInput_text')[0]
        self.input_date_end = self.browser.find_elements_by_id('ctl00_cphMainContent_txtRLEndDate_dateInput_text')[0]
        print(self.input_date_start)
        print(self.input_date_end)
        time.sleep(1)
        self.input_date_start.send_keys('1/1/2020')
        self.input_date_end.send_keys('10/4/2020')
        select = Select(self.browser.find_elements_by_id('ctl00_cphMainContent_ddlRLDocumentType_vddlDropDown')[0])
        select.select_by_visible_text('DEED')
        print('OK!')
        self.submit_button[0].click()
        time.sleep(8)
    
    def pages_counter(self):
        self.last_page_button = self.browser.find_elements_by_xpath('//*[@id="ctl00_cphMainContent_gvSearchResults"]/tbody/tr[1]/td/table/tbody/tr/td[12]/a')[0]
        self.last_page_button.click()
        self.pages_quantity = self.browser.find_elements_by_xpath('//*[@id="ctl00_cphMainContent_gvSearchResults"]/tbody/tr[1]/td/table/tbody/tr/td[12]/span')[0].text
        print('we have {} pages'.format(self.pages_quantity))
        self.first_page_button = self.browser.find_elements_by_xpath('//*[@id="ctl00_cphMainContent_gvSearchResults"]/tbody/tr[1]/td/table/tbody/tr/td[1]/a')[0]
        self.first_page_button.click()
        time.sleep(5)
        return self.pages_quantity

    def next_page(self, page):
            print('page № {} was parsed'.format(page-1))
            self.jscode = "javascript:__doPostBack('ctl00$cphMainContent$gvSearchResults','Page${}')".format(int(page))
            self.browser.execute_script(self.jscode)
            time.sleep(1)
            

    def browser_close(self):
        self.browser.close()
        

# search_doc = DocSearch()

# search_doc.search()
# pages_quantity = search_doc.pages_counter()
# time.sleep(1)
# for page in range(2, int(pages_quantity)+ 1):
#     search_doc.next_page(page)
# time.sleep(5)
# search_doc.browser_close()