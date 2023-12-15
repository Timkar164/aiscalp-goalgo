import { Injectable } from '@angular/core';
import {HTTP_API} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class CodeService {

  constructor(private http: HttpClient) { }

  checkCode(code:string){
    let formData = new FormData()
    formData.append("text",code)
    const response = this.http.post(HTTP_API+'/checkcode',formData)
    return response
  }

  runCode(requerments:any,code:any,strategy:any){
    let formData = new FormData()
    formData.append("codeFile",code,code.name)
    formData.append("requirementsFile",requerments,requerments.name)
    formData.append("sname",strategy.name)
    formData.append("sdescription",strategy.description)
    formData.append("scodetype",strategy.codetype)
    formData.append("svizible",strategy.vizible)
    formData.append("sactivtype",strategy.activtype)
    let token = localStorage.getItem("access_token")
    const response = this.http.post(HTTP_API+'/runcode?token=' + token,formData)
    return response
  }
  runEditCode(requerments:any,code:any,strategy:any){
    let formData = new FormData()
    formData.append("code",code)
    formData.append("requirementsFile",requerments,requerments.name)
    formData.append("sname",strategy.name)
    formData.append("sdescription",strategy.description)
    formData.append("scodetype",strategy.codetype)
    formData.append("svizible",strategy.vizible)
    formData.append("sactivtype",strategy.activtype)
    let token = localStorage.getItem("access_token")
    const response = this.http.post(HTTP_API+'/runcodeeditor?token=' +token,formData)
    return response
  }
}
