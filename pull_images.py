import requests
import json
import time


def get_secret():
    dat = {}
    with open('./secrets.json', 'r') as infile:
        dat = json.load(infile)
    secret = dat.get('api_key')
    if secret is None:
        raise ValueError('no valid key')
    return secret


def make_full_request(lat, lon, radius, tags, key):
    print('Getting first page.')
    res = make_request(lat, lon, radius, tags, key)
    photos = res.get('photos', {}).get('photo')
    pages = res.get('photos', {}).get('pages')
    print('Pages: {}'.format(pages))
    for i in range(1, pages):
        print('Getting page {}'.format(i))
        res = make_request(lat, lon, radius, tags, key, page=i)
        time.sleep(1)
        photos.extend(res.get('photos', {}).get('photo', []))
    return photos


def make_request(lat, lon, radius, tags, key, page=None):
    url = 'https://api.flickr.com/services/rest/'
    payload = {
        'method': 'flickr.photos.search',
        'lat': lat,
        'lon': lon,
        'radius': radius,
        'tags': tags,
        'extras': 'geo',
        'api_key': key,
        'format': 'json'
    }
    if page is not None:
        payload['page'] = page
    res = requests.get(url, params=payload)
    text_val = None
    if res.status_code == 200:
        text_val = json.loads(res.text[14:-1])
    return text_val


secret_key = get_secret()
# vals = make_full_request(50.838679, 4.2933659, 10, 'invader', secret_key)  # brussels
# vals = make_full_request(40.75206, -73.9925837, 20, 'invader', secret_key)  # nyc
# vals = make_full_request(48.86145, 2.32268, 2, 'invader', secret_key)  # paris
vals = make_full_request(51.510348, -0.1151311, 15, 'invader', secret_key)  # london

with open('london.csv', 'w') as ofile:
    ofile.write('lat, lon, title\n')
    for item in vals:
        ofile.write('{},{},{}\n'.format(item['latitude'], item['longitude'], item['title'].encode('utf8')))
