import time
import random
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

def range_sum_no_cache(array, left, right):
    return sum(array[left:right+1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, cache, left, right):
    key = (left, right)
    result = cache.get(key)
    if result == -1:
        result = sum(array[left:right+1]) 
        cache.put(key, result)
    return result

def update_with_cache(array, cache, index, value):
    array[index] = value
    for key in list(cache.cache):
        if key[0] <= index <= key[1]:
            del cache.cache[key]

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:       
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                
            if random.random() < p_hot:       
                left, right = random.choice(hot)
            else:                             
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries

n = 100_000
array = [random.randint(1, 100) for _ in range(n)]

q = 50_000
queries = make_queries(n, q)

start_time = time.time()
for qtype, arg1, arg2 in queries:
    if qtype == "Range":
        range_sum_no_cache(array, arg1, arg2)
    elif qtype == "Update":
        update_no_cache(array, arg1, arg2)
no_cache_time = time.time() - start_time

cache = LRUCache(1000)
start_time = time.time()
for qtype, arg1, arg2 in queries:
    if qtype == "Range":
        range_sum_with_cache(array, cache, arg1, arg2)  
    elif qtype == "Update":
        update_with_cache(array, cache, arg1, arg2)
with_cache_time = time.time() - start_time

print(f"Без кешу : {no_cache_time:.2f} с")  
print(f"LRU-кеш  : {with_cache_time:.2f} с (прискорення ×{no_cache_time/with_cache_time:.1f})")