import { Component, OnInit, AfterViewChecked } from '@angular/core';
import { DataService } from '../data.service';
import { Subject } from 'rxjs';

const colors: any = {
  red: {
    primary: '#ad2121',
    secondary: '#FAE3E3'
  },
  blue: {
    primary: '#1e90ff',
    secondary: '#D1E8FF'
  },
  yellow: {
    primary: '#e3bc08',
    secondary: '#FDF1BA'
  }
};

const date = new Date();
const d = date.getDate();
const m = date.getMonth();
const y = date.getFullYear();

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss']
})


export class CalendarComponent implements OnInit, AfterViewChecked {

  events$: Object;
  viewDate: Date = new Date();
  refresh: Subject<any> = new Subject();

  constructor(private data: DataService) { }

  ngOnInit() {
    this.data.getEvents().subscribe(
      data => this.events$ = data
    );
  }

  ngAfterViewChecked() {
    this.getEvents();
  }

  getEvents () {
    this.events$[0].start = new Date();
    console.log(this.events$);
    this.refresh.next();
  }

}
