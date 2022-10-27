#!/usr/bin/env python3
from concurrent import futures
from PIL import Image
import io,base64
import grpc
import lab6_pb2
import lab6_pb2_grpc

class Server(lab6_pb2_grpc.Lab6grpcServicer):
    def __init__(self):
        pass
        
    def doAdd(self, request, context):
        print(f"Receive doAdd({request.a},{request.b})")
        return lab6_pb2.addReply(c = request.a+request.b )
    
    def doDotproduct(self, request, context):
        print(f"Receive doDotproduct")
        c = 0
        for a,b in zip(request.a,request.b):
            c += a*b
        return lab6_pb2.dotproductReply(c = c)
      
    def doRawimage(self,request,context):
        print(f"Receive raw image")
        img = Image.open(io.BytesIO(request.img))
        return lab6_pb2.imageReply(width=img.size[0],height=img.size[1])
    
    def doJsonimage(self,request,context):
        print(f"Receive json image")
        img  = Image.open(io.BytesIO(base64.b64decode(request.img.encode())))
        return lab6_pb2.imageReply(width=img.size[0],height=img.size[1])

def serve():    
    print("hi im server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6grpcServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:9999')
    server.start()
    server.wait_for_termination()

serve()
