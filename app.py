#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Usage: 
python app.py <user_id>
"""
import json
import os
import requests
import sys
import concurrent.futures

def crawl(user_id, items=[]):
  url  = 'https://vine.co/api/timelines/users/' + user_id + '?size=99999'
  media = json.loads(requests.get(url).text)
  
  try:
    for item in media['data']['records']:
      items.append(item['videoUrl'])
  except Exception as e:
    print 'Error getting vines' + e
  
  return items
  
def download(url, save_dir='./'):
  if not os.path.exists(save_dir):
    os.makedirs(save_dir)
  
  base_name = url.split('/')[-1].split('?')[0]
  file_path = os.path.join(save_dir, base_name)
  
  with open(file_path, 'wb') as file:
    print 'Downloading ' + base_name
    bytes = requests.get(url).content
    file.write(bytes)
    
if __name__ == '__main__':
  user_id = sys.argv[1]
  
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url = dict( (executor.submit(download, url, './' + user_id), url) for url in crawl(user_id) )

    for future in concurrent.futures.as_completed(future_to_url):
      url = future_to_url[future]
      
      if future.exception() is not None:
        print '%r generated an exception: %s' % (url, future.exception())

