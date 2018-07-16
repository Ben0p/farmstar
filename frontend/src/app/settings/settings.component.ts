import { Component, OnInit } from '@angular/core';
import { Directive, HostListener } from '@angular/core';
// import * as screenfull from 'screenfull';
const screenfull = require('screenfull');

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {


  fullScreen: boolean;

  toggleFullScreen() {
    this.fullScreen = !this.fullScreen;
    if (screenfull.enabled) {
    screenfull.toggle();
    this.fullScreen = true;
    }
  }

  detectFullScreen() {
    if (screenfull.isFullscreen) {
      this.fullScreen = true;
    } else {
      this.fullScreen = false;
    }
    screenfull.on('change', () => {
      this.fullScreen = screenfull.isFullscreen;
    });
  }

  constructor() { }

  ngOnInit() {
    this.detectFullScreen();
  }

}
