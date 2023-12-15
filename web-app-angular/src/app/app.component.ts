import {Component, OnInit} from '@angular/core';
import {EventService} from "./servise/event.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'goalgofront';
  public menuOpen: boolean = true;
  constructor(private event: EventService) { }
  ngOnInit() {
    this.event.menudropdown.subscribe(value =>{
      this.menuOpen = value
      console.log(this.menuOpen)
    })
  }
}
