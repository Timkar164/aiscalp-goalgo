import {EventEmitter, Injectable} from '@angular/core';
import {WS_API} from "../../environments/environment";
import {EventService} from "./event.service";

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  websocket!: WebSocket;

  constructor(private events: EventService) { }


  openWebsocketConnection(user:string) {
    let token = localStorage.getItem("access_token")
    this.websocket = new WebSocket(WS_API + user + '?token=' + token);
    this.websocket.onopen = (e) => {
      console.log(e)
    }
    this.websocket.onmessage = (e) => {
      this.events.notifications.emit(JSON.parse(e.data))
      console.log(e)
    }
    this.websocket.onclose = (e) => {
      console.log(e)
    }
  }

  closeWebsoketConnection(){
    this.websocket.close()
  }


}
