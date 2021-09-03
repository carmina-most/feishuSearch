from settings import *
from settings import userAgent
from auth import read_cookie
import requests
import subprocess
import time
import platform
from util import ob_chrome_path


async def execute_search(query_string):
    cookies = read_cookie()
    search_url = api['search_list']
    headers = {'userAgent': userAgent, 'cookie': cookies}
    params = {'query': query_string, 'offset': 0, 'count': 10, 'candidates_type': 2}
    response = requests.get(url=search_url, headers=headers, params=params)
    return response_handler(response.text)


def response_handler(response):
    url_list = []
    import json
    json = json.loads(response)
    objs = json['data']['entities']['objs']
    objs = sorted(objs.items(), key=lambda x: x[1]['open_time'], reverse=True)
    for obj in objs:
        single_data = obj[1]
        minus_title = single_data['title'].replace('<em>', '').replace('</em>', '')
        time_array = time.localtime(single_data['edit_time'])
        other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        result = {
            'url': single_data['url'],
            'message': '{}\n{}在{} 更新过'.format(minus_title, single_data['edit_name'], other_style_time)
        }
        url_list.append(result)
    return url_list


def to_feishu_doc(url):
    sys_version = platform.platform()
    if sys_version.startswith("Windows"):
        path = ob_chrome_path()
    else:
        path = macos_chrome_path
    subprocess.call([path, '--no-new-window', url])
