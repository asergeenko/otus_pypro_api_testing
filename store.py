import redis
import functools
import time
import random
import json

# Constances below are for exponential backoff algorithm used in 'retry' decorator

MIN_DELAY = 0.1
MAX_DELAY = 15 * 60
DELAY_FACTOR = 2
DELAY_JITTER = 0.1

def retry(num_tries):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            delay = MIN_DELAY
            for _ in range(num_tries):
                try:
                    return f(*args, **kwargs)
                except (TimeoutError, ConnectionError) as e:
                    time.sleep(delay)
                    delay = min(delay*DELAY_FACTOR, MAX_DELAY)
                    delay = random.gauss(delay, DELAY_JITTER)
            raise ConnectionError("Connection failed after %i tries"%(num_tries,))
        return wrapper
    return decorator


class Storage:

    def __init__(self, host = "localhost", port = 6379, timeout = 3):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.server = None
        self.connect()

    def connect(self):
        self.server = redis.Redis(
            host=self.host,
            port=self.port,
            db=0,
            socket_connect_timeout=self.timeout,
            socket_timeout=self.timeout,
            decode_responses=True
        )


    def set(self, key, value):
        try:
            return self.server.set(key, value)
        except redis.exceptions.TimeoutError:
            raise TimeoutError
        except:
            raise ConnectionError

    def get(self, key):
        try:
            value = self.server.get(key)
            if value is not None:
                try:
                    return json.loads(value)
                except json.decoder.JSONDecodeError:
                    # not containing a JSON document
                    return value.decode()
        except redis.exceptions.TimeoutError:
            raise TimeoutError
        except:
            raise ConnectionError


class Store:

    max_retries = 5

    def __init__(self, storage):
        self.storage = storage
        self.cache = {}

    def cache_get(self, key):
        return self.cache.get(key)

    def cache_set(self, key, value, expires=None):
        self.cache[key] = value

    @retry(max_retries)
    def set(self, key, value):
        self.cache_set(key, value)
        return self.storage.set(key, value)

    @retry(max_retries)
    def get(self, key, use_cache_if_error = True):
        if use_cache_if_error:
            try:
                return self.storage.get(key)
            except:
                return self.cache_get(key)
        else:
            return self.storage.get(key)


