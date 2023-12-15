# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 11:38:45 2023

@author: timka
"""
import time

STATUS = ['info','warning','error','sucsess']
TYPE = ['strategy','system']

def build_notification(_type=None,message=None,status=None,active=True):
    return {
        "type":_type,
        "message":message,
        "time": int(time.time()),
        "status":status,
        "active":active,
        }