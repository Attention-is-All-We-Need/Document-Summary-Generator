import os
import sys
folder_path = os.getcwd()
sys.path.append(folder_path)
from urllib.parse import urlparse, parse_qs
from contextlib import suppress
from src.exception import CustomException
from src.logger import logging
from youtube_transcript_api import YouTubeTranscriptApi

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
    

def get_yt_id(url, ignore_playlist=False):

    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com', 'music.youtube.com'}:
        if not ignore_playlist:
            with suppress(KeyError):
                return parse_qs(query.query)['list'][0]
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    
def get_yt(url):
    try :
        response = requests.get(url)
        if response.status_code == 200:
            id = get_yt_id(url)
            transcript = YouTubeTranscriptApi.get_transcript(id)
            yt_text = ' '.join([item['text'] for item in transcript])

            return yt_text
        else:
             logging.info('URL not found. Error {}'.format(response.status_code))
            
    except Exception as e:
        raise CustomException(e,sys)