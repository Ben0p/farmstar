import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  constructor(private router: Router) {}
  showApps: boolean;
  toggleApps() {
    this.showApps = !this.showApps;
    if (this.showApps === true) {
      this.router.navigate(['apps']);
    } else {
      this.router.navigate(['']);
    }
  }
}
