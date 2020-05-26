import requests
import os
import csv
import time
import re
import json
import pprint as pp
from bs4 import BeautifulSoup as Be


def send_request(url, method="GET", payload={}):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        res = requests.request(url=url, method=method, headers=headers, data=payload)
        if res.status_code == 200:
            return res
        return send_request(url=url, method=method, payload=payload)
    except ConnectionError:
        time.sleep(10)
        return send_request(url=url, method=method, payload=payload)


def write_csv(lines, file_name):
    file = open(file_name, 'a', encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerows(lines)
    file.close()


def main():
    global_res = send_request(url='https://s3.amazonaws.com/assets.knowyourvw.com/prod/global/global.json?=1590423434582')
    global_obj = json.loads(global_res.text)
    for model_obj in global_obj['models']:
        models = model_obj['models']
        for m in models:
            model_id = m['id']
            video_request_url = 'https://s3.amazonaws.com/assets.knowyourvw.com/prod/models/{}/modeldata.json?=1590423435089'.format(model_id)
            video_response_obj = json.loads(send_request(url=video_request_url).text)
            year = video_response_obj['year']
            name = video_response_obj['name']
            videos = video_response_obj['videos']['allvideos']
            for video in videos:
                title = video['title']
                video_source = video['video_source']
                video_url = 'https://assets.knowyourvw.com/videos/{}.mp4'.format(video_source)
                thumb_url = 'https://assets.knowyourvw.com/videos/{}.jpg'.format(video_source)
                line = [year, make, name, title, video_url, thumb_url]
                pp.pprint(line)
                write_csv(lines=[line], file_name='Volkswagen_How_To.csv')


if __name__ == '__main__':
    print('----- Start -----')
    base_url = 'https://knowyourvw.com/models'
    make = 'Volkswagen'
    csv_header = ['YEAR', 'MAKE', 'MODEL', 'TITLE', 'VIDEO_URL', 'THUMBNAIL_URL']
    write_csv(lines=[csv_header], file_name='Volkswagen_How_To.csv')
    main()
    print('---- The End ----')
