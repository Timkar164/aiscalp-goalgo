import { Component, OnInit } from '@angular/core';
import {EventService} from "../../servise/event.service";
import {Router} from "@angular/router";
import {ProfileService} from "../../servise/profile.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  notification: any = []
  _evant!:any;

  username!: string;
  response!: any

  menuOpen: boolean = true;

  constructor(private event: EventService,private router: Router,private servise: ProfileService) { }

  ngOnInit(): void {
    this.event.notifications.subscribe(value=>{
      this._evant = value
      this.notification.push(value)
    })
    this.servise.getUser().subscribe(value => {
      this.response = value
      this.username = this.response.response
    })
  }

  remove(element:any){
    this.notification.shift(element)
  }

  dataToStr(time:any){
    var s = new Date(time*1000).toLocaleDateString("en-US")
    var d = new Date(time*1000).toLocaleTimeString("en-US")
    return s + ' '+ d
  }
  exit(){
    localStorage.clear()
    this.router.navigate(['','login'])

  }
  openMenu(){
    this.menuOpen=!this.menuOpen;
    this.event.menudropdown.emit(this.menuOpen);
  }
}
