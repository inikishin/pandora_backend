import json
import os

import requests
from .config import SYNC_TREE


def get_url(target, target_object):
    site = SYNC_TREE.get(target)
    if not site is None:
        return site['url'] +  SYNC_TREE[target]['objects'][target_object]['url_suffix']

    raise ValueError(f'Target: {target} with object {target_object} not found in config')


def get(target, target_object, filters={}):
    url = get_url(target, target_object)
    if url is None:
        return []

    params = ''
    if len(filters.keys()) > 0:
        params = '?'
        for param in filters.keys():
            params += f'{param}={filters[param]}&'
        params = params[:-1]

    response = requests.get(url=url + params, verify=False)

    if os.getenv('DEBUG') == 'True':
        print('Request to url:', url + params)
        print(f'Response: status: {response.status_code}, text: {response.text}')

    return json.loads(response.text) if response else []


def get_record(target, target_object, external_id):
    url = get_url(target, target_object)
    if url is None:
        return None

    url = url + '?external_id=' + str(external_id)
    response = requests.get(url=url, verify=False)

    #if os.getenv('DEBUG') == 'True':
    print('Request to url:', url)
    print(f'Response: status: {response.status_code}, text: {response.text}')

    if response:
        res_json = json.loads(response.text)
        if len(res_json) > 0:
            return res_json[0]
        else:
            print(f'No records with external_id {external_id}')

    return None


def post(target, target_object, data):
    url = get_url(target, target_object)
    if url is None:
        return []

    target_object_primary_key = SYNC_TREE[target]['objects'][target_object].get('primary_key', 'id')
    existing_record = get_record(target, target_object, data[target_object_primary_key])

    if existing_record:
        print(f'Record with ID: {data[target_object_primary_key]} already exist. Make PUT request for the data')
        put(target, target_object, data)
    else:
        request_data = data.copy()
        request_data['external_id'] = str(data[target_object_primary_key])
        if request_data.get('id'):
            request_data.pop('id')
        print(f'[POST] url: {url}, data: {request_data}')
        response = requests.post(url=url, json=request_data, verify=False)
        if response:
            print('POST response status_code:', response.status_code, response.text)


def put(target, target_object, data):
    url = get_url(target, target_object)
    if url is None:
        return []

    target_object_primary_key = SYNC_TREE[target]['objects'][target_object].get('primary_key', 'id')

    existing_record = get_record(target, target_object, data[target_object_primary_key])
    if existing_record:
        print('[POST] url', url + existing_record['id'])
        request_data = data.copy()
        request_data['external_id'] = str(data[target_object_primary_key])
        request_data.pop('id')
        response = requests.put(url=url + existing_record['id'] + '/', json=request_data, verify=False)
        if response:
            print('PUT response status_code:', response.status_code, response.text)


def delete(target, target_object, data):
    url = get_url(target, target_object)
    if url is None:
        return []

    target_object_primary_key = SYNC_TREE[target]['objects'][target_object].get('primary_key', 'id')

    existing_record = get_record(target, target_object, data[target_object_primary_key])

    if existing_record:
        print('delete url', url + existing_record['id'])
        response = requests.delete(url=url + existing_record['id'] + '/')
        if response:
            print('DELETE response status_code:', response.status_code, response.text)




# def a():
#     from api.pandora.sync import post, delete, get_record, get, put
#     from quote.models import Currency
#     c = Currency.objects.filter(code='RUB1').values()[0]
#     delete('PCM', 'quotes.currency', c)
#     post('PCM', 'quotes.currency', c)
#     put('PCM', 'quotes.currency', c)
#     quit()
#       sync('PCM', 'quotes.currency', c)
#     from api.pandora.sync import sync
# from quote.models import Ticker
# t = Ticker.objects.all().values()




