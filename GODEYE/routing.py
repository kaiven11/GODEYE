#coding=utf-8
from channels import route
from GOD import consumers
channel_routing = [
       # Wire up websocket channels to our consumers:
       route("websocket.connect", consumers.ws_connect),
       route("websocket.receive", consumers.ws_receive),
    ]
