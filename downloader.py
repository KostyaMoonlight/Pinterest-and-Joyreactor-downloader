# -*- coding: utf-8 -*-
import urllib.request
import re
import time
import os
from selenium import webdriver
import click
import json
import logging
from utils import load_cred
from browser import Browser, JoyrectorBrowser
from image_downloader import ImageDownloader, PinterestImageDownloader, JoyreactorImageDownloader


logging.basicConfig(filename="logs/logs.ini",level=logging.INFO)


def download(source, scroll_limit, path_to_save, cred_path, meta_path, log_path, downloader, _browser):
    browser = _browser(source, meta_path)  
    if cred_path:
        browser.login(cred_path)
    urls = browser.collect_urls(scroll_limit)
    image_downloader = downloader(urls, log_path, path_to_save)
    image_downloader.download()
    del browser


@click.group()
def main():
    pass

@main.command()
@click.option("--source")
@click.option("--scroll_limit", type=int, default="10000")
@click.option("--path_to_save", default="images")
@click.option("--cred_path", default="auths/pinterest.json")
@click.option("--meta_path", default="metas/pinterest.json")
@click.option("--log_path", default="logs/board_urls.txt")
def download_pinterest(source, scroll_limit, path_to_save, cred_path, meta_path, log_path):
    download(source, 
             scroll_limit, 
             path_to_save, 
             cred_path, 
             meta_path, 
             log_path, 
             PinterestImageDownloader, 
             Browser)


@main.command()
@click.option("--source")
@click.option("--scroll_limit", type=int, default="10000")
@click.option("--path_to_save", default="images")
@click.option("--meta_path", default="metas/joyreactor.json")
@click.option("--log_path", default="logs/board_urls.txt")
def download_joyreactor(source, scroll_limit, path_to_save, meta_path, log_path):
    download(source, 
             scroll_limit, 
             path_to_save, 
             None, 
             meta_path, 
             log_path, 
             JoyreactorImageDownloader, 
             JoyrectorBrowser)


@main.command()
@click.option("--source")
@click.option("--scroll_limit", type=int, default="10000")
@click.option("--cred_path", default="auths/pinterest.json")
@click.option("--meta_path", default="metas/pinterest.json")
@click.option("--log_path", default="logs/board_urls.txt")
def download_pinterest_boards(source, scroll_limit, cred_path, meta_path, log_path):
    with open(source, "r") as f:
        download_meta = json.load(f)
    for (url, path_to_save) in download_meta:       
        download(url, 
                scroll_limit, 
                path_to_save, 
                cred_path, 
                meta_path, 
                log_path, 
                PinterestImageDownloader, 
                Browser)




   
        
if __name__=="__main__":
    main()