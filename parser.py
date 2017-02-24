import sys
import os
import matplotlib.pyplot as plt
import numpy as np

f=open('me_at_the_zoo.in')
vidoes_no, endpoints_no, request_des_no, caches_no, cache_size = [int(x) for x in f.readline().split()]
video_sizes = f.readline().split()
assert len(video_sizes) == vidoes_no


endpoints = []
for endpoint in range(endpoints_no):
    endpoint_dic = {}
    endpoint_latency_dc, endpoint_cache_no = [int(x) for x in f.readline().split()]
    endpoint_dic['dc_latency'] = endpoint_latency_dc
    endpoint_dic['cache_no'] = endpoint_cache_no
    connected_caches = []
    for cache in range(endpoint_cache_no):
        cache_index, latency = [int(x) for x in f.readline().split()]
        connected_caches.append((cache_index, latency))
        endpoint_dic['caches'] = connected_caches
    endpoints.append(endpoint_dic)

requests = []
for request in range(request_des_no):
    video_index, endpoint_index, no_of_request =  [int(x) for x in f.readline().split()]
    requests.append((video_index, endpoint_index, no_of_request))



for cache:
    for connected_endpoints:
        top vidoes shared across the endpoints,
            video with

        use this for cache
            (decrease space of the cache)




print 'hi'
