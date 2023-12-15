# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 12:15:35 2023

@author: timka
"""

import bson, os
#from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import time
#load_dotenv()

DATABASE_URL=os.environ.get('DATABASE_URL')
print(DATABASE_URL)
client = MongoClient(DATABASE_URL)
db = client.myDatabase


    
class Strategy:
    def __init__(self):
        return
    
    def create(self,user_id,name,title="",description="",category=""):
        strategy = self.get_by_name(name)
        if strategy:
            return
        new_strategy = db.strategys.insert_one({
                "title": title,
                "description": description,
                "name":name,
                "category": category,
                "user_id": user_id,
                "subscribe_users":[user_id]
            })
    def get_all(self):
        strategys = db.strategy.fing()
        return [{**strategy, "_id" :str(strategy["_id"])} for strategy in strategys]
    
    def get_by_id(self, strategys_id):
        """Get a book by id"""
        strategys = db.strategys.find_one({"_id": bson.ObjectId(strategys_id)})
        if not strategys:
            return
        strategys["_id"] = str(strategys["_id"])
        return strategys
    
    def get_by_name(self,name):
        strategy = db.strategys.find_one({"name":name})
        if not strategy:
            return
        return strategy
    
    def subscribe(self,strategy_id,user_id):
        data = self.get_by_id(strategy_id)
        data['subscribe_users'].append(user_id)
        data.pop("_id")
        strategy = db.strategys.update_one({"_id": bson.ObjectId(strategy_id)},
         {
             "$set": data
         })
        strategy = self.get_by_id(strategy_id)
        return strategy
    
    def unsubscribe(self,strategy_id,user_id):
        data = self.get_by_id(strategy_id)
        if user_id in data['subscribe_users']:
            data['subscribe_users'].remove(user_id)
        data.pop("_id")
        strategy = db.strategys.update_one({"_id": bson.ObjectId(strategy_id)},
         {
             "$set": data
         })
        strategy = self.get_by_id(strategy_id)
        return strategy
        

    def delete(self, strategy_id):
        """Delete a strategy"""
        strategy = db.strategys.delete_one({"_id": bson.ObjectId(strategy_id)})
        return strategy
    

    
class User:
    """User Model"""
    def __init__(self):
        return

    def create(self, name="", email="", password=""):
        """Create a new user"""
        user = self.get_by_email_name(email,name)
        if user:
            return
        new_user = db.users.insert_one(
            {
                "name": name,
                "email": email,
                "password": self.encrypt_password(password),
                "active": True,
                "strategys":list(),
                "accounts":list(),
                "endpoints":list()
            }
        )
        return self.get_by_id(new_user.inserted_id)

    def get_all(self):
        """Get all users"""
        users = db.users.find({"active": True})
        return [{**user, "_id": str(user["_id"])} for user in users]

    def get_by_id(self, user_id):
        """Get a user by id"""
        user = db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    def get_by_email(self, email):
        """Get a user by email"""
        user = db.users.find_one({"email": email, "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user
    
    def get_by_email_name(self, email,name):
        """Get a user by email"""
        user = db.users.find_one({"email": email, "name": name,"active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user
    
    def get_by_email_password(self, email,password):
        """Get a user by email"""
        user = db.users.find_one({"email": email, "password":self.encrypt_password(password),"active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def set_user_account(self,email,broker,apikey,money):
        user = db.users.find_one({"email": email})
        if not user:
            return
        user_id = str(user["_id"])
        user["accounts"].append({"broker":broker,"apikey":apikey,"money":money,"createtime":time.time()})
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": user
            })
        user = self.get_by_id(user_id)
        for i in range(len(user["accounts"])):
            user["accounts"][i].pop('apikey')
        return user["accounts"]
    
    def delet_user_account(self,email,createtime):
        user = db.users.find_one({"email": email})
        if not user:
            return
        user_id = str(user["_id"])
        accounts = []
        for i in range(len(user['accounts'])):
            if user['accounts'][i]["createtime"]!=createtime:
                accounts.append(user['accounts'][i])
        user['accounts'] = accounts
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": user
            })
        user = self.get_by_id(user_id)
        for i in range(len(user["accounts"])):
            user["accounts"][i].pop('apikey')
        return user["accounts"]
            
        
    
    def set_user_endpoint(self,email,name,url):
        user = db.users.find_one({"email": email})
        if not user:
            return
        user_id = str(user["_id"])
        user["endpoints"].append({"name":name,"url":url,"createtime":time.time()})
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": user
            })
        user = self.get_by_id(user_id)
        return user["endpoints"]
    
    
    def delet_user_endpoint(self,email,createtime):
        user = db.users.find_one({"email": email})
        if not user:
            return
        user_id = str(user["_id"])
        enpoint = []
        for i in range(len(user['endpoints'])):
            if user['endpoints'][i]["createtime"]!=createtime:
                enpoint.append(user['endpoints'][i])
        user['endpoints'] = enpoint
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": user
            })
        user = self.get_by_id(user_id)
        return user["endpoints"]
    
    def update(self, user_id, name=""):
        """Update a user"""
        data = {}
        if name:
            data["name"] = name
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )
        user = self.get_by_id(user_id)
        return user

    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user