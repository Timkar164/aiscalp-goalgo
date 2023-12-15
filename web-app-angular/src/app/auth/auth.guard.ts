import {Injectable} from "@angular/core";
import {ActivatedRouteSnapshot, CanActivate, CanActivateChild, Router, RouterStateSnapshot} from "@angular/router";
import {AuthService} from "../servise/auth.service";

@Injectable()
export  class AuthGuard
  implements CanActivate , CanActivateChild {
  private AuthValue: any;
  private response:any;
  constructor(private router: Router,private servise: AuthService) {
  }
  async canActivate(next: ActivatedRouteSnapshot,
                    state: RouterStateSnapshot): Promise<boolean>{
    let access_token = localStorage.getItem('access_token')
    let refresh_token = localStorage.getItem('refresh_token')
    if (access_token == null){
      console.log(access_token)
      this.router.navigate(['','login'])
      return false
    }
    else {
      const auth = await this.servise.checkToken(refresh_token).toPromise()
      this.response = auth
      localStorage.setItem("access_token",this.response.access_token)
      localStorage.setItem("refresh_token",this.response.refresh_token)
      //
      // this.router.navigate([''])
      return true
    }

  }
  async canActivateChild(next: ActivatedRouteSnapshot,
                         state: RouterStateSnapshot): Promise<boolean>{
    return await this.canActivate(next,state)
  }
}
