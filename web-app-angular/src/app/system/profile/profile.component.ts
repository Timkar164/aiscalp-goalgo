import { Component, OnInit } from '@angular/core';
import {ProfileService} from "../../servise/profile.service";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  public broker!: string
  public apikey!: string
  public money!: string

  public endpointname!: string
  public endpointurl!: string

  public user!: any
  response!: any
  constructor(private servise: ProfileService) { }


  ngOnInit(): void {
    this.servise.getUserData().subscribe(value => {
      this.user = value
    })
  }

  addEndpoint(){
    this.servise.addEndpoint(this.endpointname,this.endpointurl).subscribe(value => {
      this.response = value
      this.user.endpoints =this.response.response
    })
  }
  deletEndpoint(endpoint:any){
    this.servise.deletEndpoint(endpoint).subscribe(value=>{
      this.response = value
      this.user.endpoints = this.response.response
    })
  }

  addAccaunt(){
    this.servise.addAccount(this.broker,this.apikey,this.money).subscribe(value => {
      this.response = value
      this.user.accounts = this.response.response
    })
  }
  deletAccount(account:any){
    this.servise.deletAccount(account).subscribe(value=>{
      this.response = value
      this.user.accounts = this.response.response
    })
  }

  dataToStr(time:any){
    var s = new Date(time*1000).toLocaleDateString("en-US")
    var d = new Date(time*1000).toLocaleTimeString("en-US")
    return s + ' '+ d
  }

}
