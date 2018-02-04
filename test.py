#coding=utf-8

def decorator(func):
    def wrapper(*args,**kwargs):
         if kwargs.get("file_upload",None):


        return  wrapper