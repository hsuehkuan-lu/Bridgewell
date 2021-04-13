import requests
import random
import timeit


def dsp_request():
    data = {'bid_floor': random.randint(1, 200)}
    # print(data)
    r = requests.post('http://127.0.0.1:5000/bw_dsp', data=data)
    # print(r)
    # print(r.status_code)
    # if r.status_code == 200:
    #     print(r.json())


def add_ad_request():
    r = requests.post('http://127.0.0.1:5000/add_ad_data')
    print(r)
    print(r.reason)
    print(r.text)


def delete_ad_request():
    print(requests.post('http://127.0.0.1:5000/delete_ad_data'))


def timeit_dsp_request():
    print(timeit.timeit(lambda: dsp_request(), number=1000))


timeit_dsp_request()
# dsp_request()
# delete_ad_request()
# add_ad_request()
