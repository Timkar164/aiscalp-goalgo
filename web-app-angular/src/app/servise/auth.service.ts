import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {HTTP_API} from "../../environments/environment";

@Injectable({
  providedIn: "root"
})

export class AuthService{
  constructor(private http: HttpClient) {
  }
  auth(email:string,password:string){
    const body = {email: email, password: password};
    const response = this.http.post(HTTP_API+'/login',body)
    return response
  }
  checkToken(refresh_token:any){
    const body = {refresh_token:refresh_token}
    const response = this.http.get(HTTP_API+'/refresh?token='+refresh_token)
    return response
  }

  register(name:string,email:string,password:string){
    const body = {name: name, email: email,password: password}
    const response = this.http.post(HTTP_API+'/register',body)
    return response

  }


}
