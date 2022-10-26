#!/usr/bin/env python3

from __future__ import print_function
import requests
import json,base64
import time,random
import sys
import grpc

import lab6_pb2
import lab6_pb2_grpc

if len(sys.argv) not in (3,4):
    print("usage: {} [host] operation N".format(sys.argv[0]))
    sys.exit(1)
if len(sys.argv) == 3:
    host,operation,N = 'localhost',sys.argv[1],int(sys.argv[2])
else:
    host,operation,N = sys.argv[1],sys.argv[2],int(sys.argv[3])

channel = grpc.insecure_channel('{}:9999'.format(host))
stub = lab6_pb2_grpc.Lab6grpcStub(channel)

start = time.perf_counter()
for i in range(N):
    if operation == 'add':
        hreq = lab6_pb2.addRequest(a=5,b=10)
        reply = stub.doAdd(hreq)
        # print(f'sum is {reply.c}')
    if operation == 'dotproduct':
        hreq = lab6_pb2.dotproductRequest()
        hreq.a.extend([random.random() for _ in range(100)])
        hreq.b.extend([random.random() for _ in range(100)])
        reply = stub.doDotproduct(hreq)
        # print(f'sum is {reply.c}')
    if operation == 'rawimage':
        img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
        hreq = lab6_pb2.rawimageRequest(img=img)
        reply = stub.doRawimage(hreq)
        # print(f'Width = {reply.width}, height = {reply.height}')
    if operation == 'jsonimage':
        img = base64.b64encode(open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()).decode()
        hreq = lab6_pb2.jsonimageRequest(img=img)
        reply = stub.doJsonimage(hreq)
        # print(f'Width = {reply.width}, height = {reply.height}')
delta = ((time.perf_counter() - start)/N)*1000
print(f"{operation}: Took", delta, "ms per operation")