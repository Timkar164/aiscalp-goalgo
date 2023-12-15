import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../servise/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  name!: string;
  email!: string;
  password!: string;
  data!: any;
  constructor(private servise: AuthService,private router: Router) { }

  ngOnInit(): void {
  }

  register(){
    this.servise.register(this.name,this.email,this.password).subscribe(value => {
      this.data = value
      localStorage.setItem("access_token",this.data.access_token)
      localStorage.setItem("refresh_token",this.data.refresh_token)
      this.router.navigate([''])
    })
  }
}
