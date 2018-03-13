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
        photos.append(res.get('photos', {}).get('photo', []))
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
vals = make_full_request(48.86145, 2.32268, 2, 'invader', secret_key)
with open('output.json', 'w') as ofile:
    for item in vals:
        ofile.write('{}\n'.format(json.dumps(item)))
