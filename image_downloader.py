import logging
import os
import re
import urllib
from tqdm import tqdm
import socket

timeout = 20
socket.setdefaulttimeout(timeout)

class ImageDownloader:
    def __init__(self, urls, log_path, path_to_save):
        self.urls = urls
        self.log_path = log_path
        self.path_to_save = path_to_save
        
    def download(self):
        self._filter_images()
        self._get_full_size_images()
        self._filter_images()
        if self.log_path:
            self.__log_images_path()
        self.__download_images()


    def _filter_images(self):
        self.urls = list(set(self.urls))
        self.urls = list(filter(None, self.urls))
        logging.info(f"Collected {len(self.urls)} urls.")
       

    def _get_full_size_images(self):
        pass
        

    def __log_images_path(self):
        with open(self.log_path, 'w') as f:
            for url in self.urls:
                f.write(f"{url}\n")

    def _restore_image_path(self, url):
        return url

    def __download_images(self):
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)
        for i, url in enumerate(tqdm(self.urls)):
            try:
                urllib.request.urlretrieve(url, f"{self.path_to_save}/{str(i)}-image.{url.split('.')[-1]}")
            except:
                logging.warning(f"Link({url}) is broken.")       
                try:
                    urllib.request.urlretrieve(self._restore_image_path(url), f"{self.path_to_save}/{str(i)}-image.{url.split('.')[-1]}")      
                except:
                    logging.warning(f"Link({url}) is broken.")       
                    
                
        logging.info("Images downloded.")

class PinterestImageDownloader(ImageDownloader):
    def __init__(self, urls, log_path, path_to_save):
        super().__init__(urls, log_path, path_to_save)

    def _filter_images(self):
        for i in range(len(self.urls)):
            if(self.urls[i][-4:]!=".jpg" or "_RS" in self.urls[i]):
                self.urls[i]= ""
        print(len(self.urls))
        self.urls = list(set(self.urls))
        print(len(self.urls))
        self.urls = list(filter(None, self.urls))
        logging.info(f"Collected {len(self.urls)} urls.")
       

    def _restore_image_path(self, url):
        return self.urls_backup[url]

    def _get_full_size_images(self):
        self.urls_backup = {}
        self.original_images = list(self.urls)
        for i in range(len(self.urls)):
            #TODO: Validate      
            original = self.urls[i]
            if '/originals/' not in self.urls[i]:
                self.urls[i]=re.sub('.com/.*?/','.com/originals/',self.urls[i],flags=re.DOTALL)
            self.urls_backup[self.urls[i]]=original
        

class JoyreactorImageDownloader(ImageDownloader):
    def __init__(self, urls, log_path, path_to_save):
        super().__init__(urls, log_path, path_to_save)

    def _filter_images(self):
        self.urls = list(set(self.urls))
        self.urls = list(filter(None, self.urls))
        logging.info(f"Collected {len(self.urls)} urls.")
       

        
