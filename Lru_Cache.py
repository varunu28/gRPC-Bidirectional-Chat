from collections import OrderedDict
import time
import itertools


class Lru_Cache:

    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def set(self, key, value):
        # if key in self.cache:
        #     self.cache.pop(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def print_cache(self):
        # keys = list(self.cache.keys())
        # print(keys)
        return list(self.cache.values())

    def cache_len(self):
        return len(self.cache)

    def delete_old_message(self, limit):
        count = 0
        i = 0
        while i < len(self.cache):
            keys = list(self.cache.keys())
            if len(keys) == 0:
                break
            if int(time.time() - float(keys[i])) >= limit:
                count = count + 1
                if len(self.cache) > 0:
                    self.cache.popitem(last=False)
            else:
                break

        return count