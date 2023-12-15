import { Component, OnInit } from '@angular/core';
import {WebSocketService} from "../servise/web-socket.service";
import {ProfileService} from "../servise/profile.service";

@Component({
  selector: 'app-system',
  templateUrl: './system.component.html',
  styleUrls: ['./system.component.css']
})
export class SystemComponent implements OnInit {
  public response!: any;
  constructor(private ws:WebSocketService,private servise:ProfileService) { }

  ngOnInit(): void {
    this.servise.getUser().subscribe(value => {
      this.response = value
      this.ws.openWebsocketConnection(this.response.response)
    })

  }

}
