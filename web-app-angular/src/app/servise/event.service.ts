import { Injectable, EventEmitter} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  notifications = new EventEmitter<any>();
  menudropdown = new EventEmitter<any>();
  constructor() { }
}
