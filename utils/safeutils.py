#encoding: utf-8

from urllib.parse import urlparse,urljoin
from flask import request

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    # ParseResult(scheme='http', netloc='127.0.0.1:8000', path='/front/', params='', query='', fragment='')
    test_url = urlparse(urljoin(request.host_url, target))
    # urljoin('http://127.0.0.1:8000/front/', 'http://127.0.0.1:8000/') ==> http://127.0.0.1:8000/
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc