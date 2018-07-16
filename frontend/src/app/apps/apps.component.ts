import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-apps',
  templateUrl: './apps.component.html',
  styleUrls: ['./apps.component.scss']
})
export class AppsComponent implements OnInit {

  constructor(private router: Router) { }
  toggle (content) {
    console.log(content);
    this.router.navigate([content]);
  }
  ngOnInit() {
  }

}
