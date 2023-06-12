import os
import sys
folder_path = os.getcwd()
sys.path.append(folder_path)

from src.exception import CustomException
from src.logger import logging

import requests
from bs4 import BeautifulSoup

def get_website(url):
    try :
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            article_title = soup.find('h1').get_text()
            paragraphs = soup.find_all('p')

            article_text = '\n'.join([p.get_text() for p in paragraphs])
            
            return article_title+ " "+article_text
        else:
            logging.info('URL not found. Error {}'.format(response.status_code))
            
    except Exception as e:
        raise CustomException(e,sys)