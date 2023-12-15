# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 12:14:09 2023

@author: timka
"""
import uvicorn
import time
import os
from typing import Annotated
from fastapi import FastAPI , WebSocket, Depends, Request, HTTPException , Query, Form, UploadFile
from typing import List
from fastapi.responses import HTMLResponse , JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect
from asyncio import Queue

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from models import User
from pydantic import BaseModel
from playgraund import evaluate_pylint
from notification import build_notification
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = []
message_queure = dict()
code_queure = dict()

import subprocess

class Settings(BaseModel):
    authjwt_secret_key: str = 'jsksjFjsksajdahh'
    
class UserModel(BaseModel):
    email: str
    password: str
    
class UserRegisterModel(BaseModel):
    name: str
    email: str
    password: str
    
class UserCreditails(BaseModel):
    broker: str
    apikey: str
    money: int
    
class UserEndpoint(BaseModel):
    name: str
    url: str
    
class Endpoint(BaseModel):
    name: str
    url: str
    createtime: float
    
class Account(BaseModel):
    broker: str
    money: int
    createtime: float
    
class StrategyModel(BaseModel):
    name: str
    description: str
    vizible: str
    codetype: str
    activtype: str
    
@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code,contend={"detail":exc.message})
    
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, token: str = Query(...), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket",token=token)
        current_user =  Authorize.get_raw_jwt(token)
        if User().get_by_email(current_user['sub'])['name']!=username:
            raise AuthJWTException("Invalid user")
        connected_clients.append({"websocket":websocket,"username":username})
        welcome_message = build_notification(_type='system',message='Connected',status='info',active=False)
        if username in message_queure.keys():
            pass
        else:
            message_queure[username] = Queue()
        await websocket.send_json(welcome_message)
        try:
            while True:
                message =  await message_queure[username].get()
                await websocket.send_json(message)
        except WebSocketDisconnect:
            connected_clients.remove({"websocket":websocket,"username":username})
    except AuthJWTException as err:
        await websocket.send_json(build_notification(_type='system',message='Not connected',status='error',active=True))
        await websocket.close()
           
@app.get('/adminbroker/{message}/{username}')
async def add_system_message(message: str,username: str):
    if username in message_queure.keys():
        pass
    else:
        message_queure[username] = Queue()
    await message_queure[username].put(message)
    return {}


@app.websocket("/ws/code/{username}")
async def websocket_code_endpoint(websocket: WebSocket, username: str, token: str = Query(...), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket",token=token)
        current_user =  Authorize.get_raw_jwt(token)
        if User().get_by_email(current_user['sub'])['name']!=username:
            raise AuthJWTException("Invalid user")
        connected_clients.append({"websocket":websocket,"username":username})
        welcome_message = "ws connected"
        if username in code_queure.keys():
            pass
        else:
            code_queure[username] = Queue()
        await websocket.send_text(welcome_message)
        try:
            while True:
                message =  await code_queure[username].get()
                await websocket.send_json(message)
                if message == 'code exit':
                    websocket.close()
        except WebSocketDisconnect:
            connected_clients.remove({"websocket":websocket,"username":username})
    except AuthJWTException as err:
        await websocket.send_test("ws unconnected")
        await websocket.close()
        
@app.get('/admincode/{message}/{username}')
async def add_code_message(message: str,username: str):
    if username in code_queure.keys():
        pass
    else:
        code_queure[username] = Queue()
    await code_queure[username].put(message)
    return {}

@app.post('/login')
def login(user: UserModel, Authorize: AuthJWT = Depends()):
    if User().login(user.email,user.password):
        access_token = Authorize.create_access_token(subject=user.email,fresh=True)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        return {"access_token":access_token,"refresh_token":refresh_token}
    else:
        raise HTTPException(status_code=401,detail='Bad username or password')
        
@app.post('/register')
def register(user: UserRegisterModel, Authorize: AuthJWT = Depends()):
    if User().create(user.name,user.email,user.password):
        access_token = Authorize.create_access_token(subject=user.email,fresh=True)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        return {"access_token":access_token,"refresh_token":refresh_token}
    else:
        raise HTTPException(status_code=401,detail='Bad username or password')
        
@app.get('/refresh')
def refresh(token: str = Query(...), Authorize: AuthJWT = Depends()):
    current_user =  Authorize.get_raw_jwt(token)
    #print(current_user)
    if User().get_by_email(current_user['sub']):
        access_token = Authorize.create_access_token(subject=current_user['sub'],fresh=True)
        refresh_token = Authorize.create_refresh_token(subject=current_user['sub'])
        return {"access_token":access_token,"refresh_token":refresh_token}
    else:
        raise HTTPException(status_code=401,detail='Bad username or password')
        

@app.post('/addaccount')
def add_account(creditails: UserCreditails, token: str = Query(...), Authorize: AuthJWT = Depends()):
         try:
             Authorize.jwt_required("websocket",token=token)
             current_user =  Authorize.get_raw_jwt(token)
             accounts = User().set_user_account(current_user['sub'], creditails.broker, creditails.apikey, creditails.money)
             if accounts:
                 return {"response":accounts}
             else:
                 raise HTTPException(status_code=401,detail='cannot add')
         except AuthJWTException as err:
             raise HTTPException(status_code=401,detail='user not auth')
             
@app.post('/deletaccount')
def delet_account(account: Account, token: str = Query(...), Authorize: AuthJWT = Depends()):
         try:
             Authorize.jwt_required("websocket",token=token)
             current_user =  Authorize.get_raw_jwt(token)
             accounts = User().delet_user_account(current_user['sub'], account.createtime)
             return {"response":accounts}
         except AuthJWTException as err:
             raise HTTPException(status_code=401,detail='user not auth')
             
@app.post('/addendpoint')
def add_endpoint(endpoint: UserEndpoint, token: str = Query(...), Authorize: AuthJWT = Depends()):
         try:
             Authorize.jwt_required("websocket",token=token)
             current_user =  Authorize.get_raw_jwt(token)
             endpoints = User().set_user_endpoint(current_user['sub'], endpoint.name, endpoint.url)
             if endpoints:
                 return {"response":endpoints}
             else:
                 raise HTTPException(status_code=401,detail='cannot add')
         except AuthJWTException as err:
             raise HTTPException(status_code=401,detail='user not auth')
             
@app.post('/deletendpoint')
def delet_endpoint(endpoint: Endpoint, token: str = Query(...), Authorize: AuthJWT = Depends()):
         try:
             Authorize.jwt_required("websocket",token=token)
             current_user =  Authorize.get_raw_jwt(token)
             endpoints = User().delet_user_endpoint(current_user['sub'], endpoint.createtime)
             return {"response":endpoints}
         except AuthJWTException as err:
             raise HTTPException(status_code=401,detail='user not auth')
             
@app.get('/getuser')
def getuser(token: str = Query(...), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required("websocket",token=token)
        current_user =  Authorize.get_raw_jwt(token)
        user = User().get_by_email(current_user['sub'])
        return {"response": user['name']}
    except AuthJWTException as err:
        raise HTTPException(status_code=401,detail='user not auth')
        
@app.get('/getuserData')
def getuserData(token: str = Query(...), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required("websocket",token=token)
        current_user =  Authorize.get_raw_jwt(token)
        user = User().get_by_email(current_user['sub'])
        if user:
            user.pop("_id")
            user.pop("password")
            for accounts in user['accounts']:
                accounts.pop("apikey")
            return user
        else:
            raise HTTPException(status_code=401,detail='user not found')
    except AuthJWTException as err:
        raise HTTPException(status_code=401,detail='user not auth')

@app.post("/checkcode")
async def check_code(text: Annotated[str, Form()]):
    output = evaluate_pylint(text)
    return {"items":output}

@app.post("/runcode")
async def run_code(requirementsFile: UploadFile,codeFile: UploadFile,\
                   sname: Annotated[str, Form()], \
                       sdescription: Annotated[str, Form()], \
                           svizible: Annotated[str, Form()], \
                               scodetype: Annotated[str, Form()], \
                                   sactivtype: Annotated[str, Form()],
                                   token: str = Query(...), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required("websocket",token=token)
        current_user =  Authorize.get_raw_jwt(token)
        current_user =  Authorize.get_raw_jwt(token)
        user = User().get_by_email(current_user['sub'])['name']
        filename = f'uploadfiles/{user}/{int(time.time())}/'
        rfile = filename + requirementsFile.filename
        cfile = filename + codeFile.filename
        
        dir_name = os.path.dirname(rfile)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        dir_name = os.path.dirname(cfile)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(rfile,"wb") as req:
            req.write(requirementsFile.file.read())
        with open(cfile,"wb") as req:
            req.write(codeFile.file.read())
        code_queure['admin'] = Queue()
        return {"items":"start"}
    except AuthJWTException as err:
        raise HTTPException(status_code=401,detail='user not auth')

@app.post("/runcodeeditor")
async def run_code_editor(requirementsFile: UploadFile,code: Annotated[str, Form()],\
                   sname: Annotated[str, Form()], \
                       sdescription: Annotated[str, Form()], \
                           svizible: Annotated[str, Form()], \
                               scodetype: Annotated[str, Form()], \
                                   sactivtype: Annotated[str, Form()],
                                   token: str = Query(...), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required("websocket",token=token)
        current_user =  Authorize.get_raw_jwt(token)
        user = User().get_by_email(current_user['sub'])['name']
        filename = f'uploadfiles/{user}/{int(time.time())}/'
        rfile = filename + requirementsFile.filename
        cfile = filename + str(int(time.time())) + '.py'
        
        dir_name = os.path.dirname(rfile)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        dir_name = os.path.dirname(cfile)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(rfile,"wb") as req:
            req.write(requirementsFile.file.read())
        with open(cfile,"w") as req:
            req.write(code)
        code_queure['admin'] = Queue()
        return {"items":"start"}
    except AuthJWTException as err:
        raise HTTPException(status_code=401,detail='user not auth')