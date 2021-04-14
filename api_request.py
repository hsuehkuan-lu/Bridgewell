import requests
import random
import timeit
from config import Config
API_HOST = Config.API_URL


def dsp_request():
    data = {'bid_floor': random.randint(1, 200)}
    print(data)
    r = requests.post(f'{API_HOST}/bw_dsp', data=data)
    print(r)
    print(r.status_code)
    if r.status_code == 200:
        print(r.json())


def add_ad_request():
    r = requests.post(f'{API_HOST}/add_ad_data')
    print(r)
    print(r.reason)
    print(r.text)


def delete_ad_request():
    print(requests.post(f'{API_HOST}/delete_ad_data'))


def timeit_dsp_request():
    print(timeit.timeit(lambda: dsp_request(), number=1000))


# timeit_dsp_request()
dsp_request()
# delete_ad_request()
# add_ad_request()
