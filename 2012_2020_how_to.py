import requests
import os
import csv
from bs4 import BeautifulSoup
import time
import json


def write_csv(lines, file_name):
    file = open(file_name, 'a', encoding="utf-8", newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerows(lines)
    file.close()


def send_request(url, method="GET", payload={}):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/81.0.4044.138 Safari/537.36'
        }
        res = requests.request(method, url=url, headers=headers, data=payload)
        if res.status_code == 200:
            return res
        return send_request(url=url, method=method)
    except ConnectionError:
        time.sleep(10)
        return send_request(url=url, method=method)


def get_models(year):
    model_url = 'https://volvo.custhelp.com/ci/ajax/widget/custom/utils/OwnersManualsPickerRD/LookupModels'
    data = {
        'w_id': 5,
        'year': year
    }
    models = []
    response = json.loads(send_request(url=model_url, method='POST', payload=data).text)['modeldata']
    for res in response:
        models.append(res['model'])
    return models


def parse(year, model):
    base_url = 'https://volvo.custhelp.com/app/manuals/ownersmanualVideo/year/{}/model/{}'.format(year, model)
    print(base_url)
    res = send_request(url=base_url)
    soup = BeautifulSoup(res.text, 'html5lib')
    wrappers = soup.find_all(attrs={'class': 'OMVideoLinkWrapper'})
    for wrapper in wrappers:
        title_soup = wrapper.find(attrs={'class': 'VideoCaption'})
        if title_soup:
            title = title_soup.text.strip()
        else:
            title = ''
        image_soup = wrapper.find('img')
        if image_soup and image_soup.has_attr('src'):
            thumb = image_soup['src']
        else:
            thumb = ''
        video_soup = soup.find(id='{}player'.format(image_soup['id']))
        if video_soup:
            video_url = video_soup.find('source')['src']
        else:
            video_url = ''
        line = [year, 'Volvo', model, title, video_url, thumb]
        print(line)
        write_csv(lines=[line], file_name=file_name)


def main():
    for year in range(2012, 2021):
        model_list = get_models(year=year)
        for model in model_list:
            parse(year=year, model=model)


if __name__ == '__main__':
    print('------- Start -------')
    csv_header = [['YEAR', 'MAKE', 'MODEL', 'TITLE', 'VIDEO_URL', 'THUMB_URL']]
    file_name = '2012_2020_Volvo_How_To.csv'
    write_csv(lines=csv_header, file_name=file_name)
    main()
    print('------ The End -------')