import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {HTTP_API} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  constructor(private http: HttpClient) { }

  addEndpoint(name: string,url: string){
    let body = {name:name,url:url}
    let token = localStorage.getItem("access_token")
    const request = this.http.post(HTTP_API+'/addendpoint?token='+token,body)
    return request
  }
  deletEndpoint(endpoint:any){
    let body = {name:endpoint.name,url:endpoint.url,createtime:endpoint.createtime}
    let token = localStorage.getItem("access_token")
    const request = this.http.post(HTTP_API+'/deletendpoint?token='+token,body)
    return request
  }

  addAccount(broker:string,apikey:string,money:string){
    let body = {broker:broker,apikey:apikey,money: money}
    let token = localStorage.getItem("access_token")
    const request = this.http.post(HTTP_API+'/addaccount?token='+token,body)
    return request
  }
  deletAccount(account:any){
    let body = {broker:account.broker,money: account.money, createtime:account.createtime}
    let token = localStorage.getItem("access_token")
    const request = this.http.post(HTTP_API+'/deletaccount?token='+token,body)
    return request
  }

  getUser(){
    let token = localStorage.getItem("access_token")
    const request = this.http.get(HTTP_API+'/getuser?token='+token)
    return request
  }
  getUserData(){
    let token = localStorage.getItem("access_token")
    const request = this.http.get(HTTP_API+'/getuserData?token='+token)
    return request
  }

}
