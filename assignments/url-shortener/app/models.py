# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata

import time

url_store = {}

def save_url(short_code, long_url):
    url_store[short_code] = {
        "long_url": long_url,
        "clicks": 0,
        "created_at": time.strftime('%Y-%m-%dT%H:%M:%S')
    }

def get_url(short_code):
    return url_store.get(short_code)

def increment_click(short_code):
    if short_code in url_store:
        url_store[short_code]['clicks'] += 1

def get_stats(short_code):
    return url_store.get(short_code)
