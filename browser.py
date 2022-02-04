import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
import re
from utils import load_cred


class Browser:
    def __init__(self, source, meta_path):
        with open(meta_path, "r") as f:
            self.meta = json.load(f)
        self.browser = webdriver.Firefox(executable_path='D:\\code\\drivers\\geckodriver.exe')
        self.browser.get(source)

    def login(self, cred_path):
        email, password = load_cred(cred_path)
        logging.info("Init logging.")
        time.sleep(3)
        self.browser.find_element_by_css_selector(self.meta["login_button"]).click()
        time.sleep(1)
        self.browser.find_element_by_id('email').send_keys(email)
        self.browser.find_element_by_id('password').send_keys(password)
        time.sleep(1)
        self.browser.find_element_by_css_selector(self.meta["signup_button"]).click()
        time.sleep(5)
        logging.info("Successful.")

    def _scroll(self):
        page_length = self.browser.execute_script(self.meta["scroll_script"])
        logging.info("Scrolling...")
        time.sleep(1)
        return page_length

    def _mini_scroll(self, position):
        page_length = self.browser.execute_script(self.meta["mini_scroll_script"]
                                                  .format(to=int(position+self.scroll_size*0.95)))
        logging.info("Scrolling...")
        time.sleep(1)
        return page_length

    def collect_urls(self, scroll_limit):
        self.scroll_size = self.browser.execute_script(self.meta["get_scroll_size"])
        page_length = self.browser.execute_script(self.meta["page_size"])
        urls = set()
        urls.update(re.findall(self.meta["image_url_pattern"], self.browser.page_source))
        match=False
        positionY = 0
        while(not match and scroll_limit): 
            scroll_limit = scroll_limit-1
            time.sleep(1)
            page_length = self._mini_scroll(positionY)
            positionY = self.browser.execute_script(self.meta["positionY"])
            urls.update(re.findall(self.meta["image_url_pattern"], self.browser.page_source))
            match =self.scroll_size*1.1+ positionY>=page_length
        logging.info("Urls collected.")
        return list(urls)

    def __del__(self):
        self.browser.quit()


class JoyrectorBrowser(Browser):
    def __init__(self, source, meta_path):
        super().__init__(source, meta_path)

    def __unfold(self):
        self.browser.execute_script(self.meta["unfold_script"])

        
    def collect_urls(self, scroll_limit):
        match=False
        urls = []
        while(not match and scroll_limit): 
            scroll_limit = scroll_limit-1
            time.sleep(5)
            self.__unfold()
            urls.extend(self.browser.execute_script(self.meta["get_images_script"]))
            if self.browser.find_element_by_css_selector(self.meta["next"]):
                self.browser.find_element_by_css_selector(self.meta["next"]).click()
                match = False
        logging.info("Urls collected.")
        return urls