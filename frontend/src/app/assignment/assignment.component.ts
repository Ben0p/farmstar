import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-assignment',
  templateUrl: './assignment.component.html',
  styleUrls: ['./assignment.component.scss']
})
export class AssignmentComponent implements OnInit {

  farms: string[] = [
    'This One',
    'That One',
    'Other One'
  ];
  fields: string[] = [
    'This Field',
    'That Field',
    'Other Field'
  ];
  tasks: string[] = [
    'seeding',
    'spraying',
    'harvesting'
  ];
  tracks: string[] = [
    'you',
    'vehicles',
    'kangaroos'
  ];

  selected = 'option2';

  spraying: boolean;
  seeding: boolean;
  harvesting: boolean;

  enabled(task) {
    console.log(task);
    if (task === 'spraying') {
      this.spraying = false; // Disabled: false
      this.seeding = true; // Disabled: true
      this.harvesting = true; // Disabled: true
    } else if (task === 'seeding') {
      this.spraying = true;
      this.seeding = false;
      this.harvesting = true;
    } else if (task === 'harvesting') {
      this.spraying = true;
      this.seeding = true;
      this.harvesting = false;
    }
  }

  constructor() { }

  ngOnInit() {
    this.spraying = false;
}
}
