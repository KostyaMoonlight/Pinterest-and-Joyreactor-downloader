# Pinterest and Joyreactor image downloader

## Install
1. Install requirments.
"""
conda create --name <env> --file requirments.txt
"""
2. Install Firefox browser.
3. Download and add geckodriver to your PATH (https://medium.com/dropout-analytics/selenium-and-geckodriver-on-mac-b411dbfe61bc)
4. Change auth credentials.

## Run examples
1. Pinterest
"""
python downloader.py download-pinterest --source https://www.pinterest.com/kostya5391/nier/    --path_to_save nier
"""
2. Joyreactor
"""
python downloader.py download-joyreactor --source http://joyreactor.cc/tag/котэ --scroll_limit 2 --path_to_save cats
"""