# Copyright 2022 Thijs Raymakers
#
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.

from podimo.config import *
from typing import Dict, Tuple
from time import time
from diskcache import Cache
from os.path import join

# Store the authentication token in a dictionary
# so it is not necessary to request a new token for every request. The key is
# derived from the provided username and password (see the `token_key` function).
TOKENS = dict()
if STORE_TOKENS_ON_DISK:
    TOKENS = Cache(join(CACHE_DIR, 'tokens_cache'))

# Give each user its own cookie jar to keep track of cookies that are
# being set and used between different requests.
cookie_jars = dict()

url_cache = Cache(join(CACHE_DIR, 'url_cache'))
podcast_cache = Cache(join(CACHE_DIR, 'podcast_cache'))

# Podcast players support the display of the file size of each episode.
# Podimo does not provide this information directly, so we do a HEAD request
# to the episode file locations. This gives us the Content-Length which is
# the file size of the episode. The file size of an episode doesn't change often,
# which makes it perfect for caching.
head_cache = Cache(join(CACHE_DIR, 'head_cache'))

def getCacheEntry(key: str, cache, delete=True):
    if key in cache:
        timestamp, value = cache[key]
        if timestamp < time():
            if delete:
                del cache[key]
            return None
        else:
            return value

def getHeadEntry(id: str):
    return getCacheEntry(id, head_cache, False)

def insertCacheEntry(key, value, timeout, cache):
    cache[key] = (time() + timeout, value)

def insertIntoTokenCache(key, value):
    insertCacheEntry(key, value, TOKEN_CACHE_TIME, TOKENS)

def insertIntoHeadCache(key, content_length, content_type):
    insertCacheEntry(key, (content_length, content_type), HEAD_CACHE_TIME, head_cache)

def insertIntoPodcastCache(key, podcast):
    insertCacheEntry(key, podcast, PODCAST_CACHE_TIME, podcast_cache)

