import urllib.parse
import hashlib
import hmac
import base64
import time
import os
import requests
from config import *

def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

# DATA uri_path, data, api_key, api_sec
def request_post(data):
    headers = {}
    headers['API-Key'] = data['api_key']
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(data['path'], data['data'], data['api_secret'])             
    req = requests.post((API_URL + data['path']), headers=headers, data=data['data'])
    return req

def request_get(data):
    headers = {}
    headers['API-Key'] = data['api_key']
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = data['api_secret']             
    req = requests.get((API_URL + data['path']), headers=headers, data=data['data'] if 'data' in data else {})
    return req

def show_info(i):
    print('ASSET: {}'.format(i['asset']))
    print('USING: {}'.format(i['using']))
    print('c: {}'.format(i['p']))