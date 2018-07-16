import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';


@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.scss']
})



export class ContactComponent implements OnInit {

  users$: Object;
  userAlert: boolean;

  constructor(private data: DataService) { }

  ngOnInit() {
    this.data.getUsers().subscribe(
      data => this.users$ = data
    );
  }

  hasAlert(user) {
    if (user.alerts > 0) {
      return (false);
    } else {
      return (true);
    }
  }
}
