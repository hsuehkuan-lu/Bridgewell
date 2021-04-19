import requests
import random
import timeit
from config import API_URL


def gql_request():
    q = '''
    query bwDsp($bidFloor: Int!){
        bwDsp(bidFloor: $bidFloor) {
            adId
            price
        }
    }
    '''
    v = {'bidFloor': random.randint(1, 50)}
    r = requests.post(f'{API_URL}/graphql', json={
        'query': q, 'variables': v
    })
    print(r)
    print(r.json())


def dsp_request():
    data = {'bid_floor': random.randint(1, 200)}
    # print(data)
    r = requests.post(f'{API_URL}/bw_dsp', data=data)
    # print(r)
    # print(r.status_code)
    # if r.status_code == 200:
    #     print(r.json())


def add_ad_request():
    r = requests.post(f'{API_URL}/add_ad_data')
    print(r)
    print(r.reason)
    print(r.text)


def delete_ad_request():
    print(requests.post(f'{API_URL}/delete_ad_data'))


def timeit_dsp_request():
    number = 1
    t = timeit.timeit(lambda: dsp_request(), number=number)
    print(f"Cost time in total {number} requests: {t}")


gql_request()
# timeit_dsp_request()
# dsp_request()
# delete_ad_request()
# add_ad_request()
