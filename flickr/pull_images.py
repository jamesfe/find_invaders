import requests
import json
import time
from os import path
import math


sfile = '../secrets/secrets.json'
output_dir = '../data/'


def output_fname():
    return str(int(time.time())) + '_output.json'


min_lat = 48
max_lat = 49
min_lon = 2
max_lon = 3
lat_delta = .1
lon_delta = .1


class flickr_getter(object):

    def __init__(self, secrets_file):
        self.sleep_time = 1
        self.secret = self.get_secret(secrets_file)

    def get_secret(self, secrets_file):
        dat = {}
        with open(secrets_file, 'r') as infile:
            dat = json.load(infile)
        secret = dat.get('api_key')
        if secret is None:
            raise ValueError('no valid key')
        return secret

    def make_full_request(self, lat, lon, radius, tags):
        print('Getting first page.')
        res = self.make_request(lat, lon, radius, tags)
        photos = res.get('photos', {}).get('photo')
        pages = res.get('photos', {}).get('pages')
        print('Pages: {}'.format(pages))
        for i in range(1, pages):
            print('Getting page {}'.format(i))
            res = self.make_request(lat, lon, radius, tags, page=i)
            time.sleep(self.sleep_time)
            photos.extend(res.get('photos', {}).get('photo', []))
        return photos

    def make_request(self, lat, lon, radius, tags, page=None):
        url = 'https://api.flickr.com/services/rest/'
        payload = {
            'method': 'flickr.photos.search',
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'tags': tags,
            'extras': 'geo',
            'api_key': self.secret,
            'format': 'json'
        }
        if page is not None:
            payload['page'] = page
        res = requests.get(url, params=payload)
        text_val = None
        if res.status_code == 200:
            text_val = json.loads(res.text[14:-1])
        return text_val


flickr = flickr_getter(sfile)

for clat in [min_lat + (lat_delta * step) for step in range(0, math.ceil((max_lat - min_lat) / lat_delta))]:
    for clon in [min_lon + (lon_delta * step) for step in range(0, math.ceil((max_lon - min_lon) / lon_delta))]:
        print('working on {}, {}'.format(clat, clon))
        vals = flickr.make_full_request(clat, clon, 20, 'invader')
        if len(vals) > 0:
            with open(path.join(output_dir, output_fname()), 'w') as ofile:
                for item in vals:
                    ofile.write('{}\n'.format(json.dumps(item)))

# vals = flickr.make_full_request(48.86145, 2.32268, 2, 'invader')
