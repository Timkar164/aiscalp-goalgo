import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../servise/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  email!: any;
  password!: any;
  data!:any;
  constructor(private servise: AuthService,private router: Router) { }

  ngOnInit(): void {
  }
  auth(){
    this.servise.auth(this.email,this.password).subscribe(value => {
      this.data = value
      localStorage.setItem("access_token",this.data.access_token)
      localStorage.setItem("refresh_token",this.data.refresh_token)
      this.router.navigate([''])
    })
  }

}
