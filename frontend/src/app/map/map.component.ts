import { Component, OnInit, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class MapComponent implements OnInit {

  loadScripts() {
    const dynamicScripts = [
      'https://api.tiles.mapbox.com/mapbox-gl-js/v0.46.0/mapbox-gl.js',
    ];
    for (let i = 0; i < dynamicScripts.length; i++) {
      const node = document.createElement('script');
      node.src = dynamicScripts[i];
      node.type = 'text/javascript';
      node.async = false;
      node.charset = 'utf-8';
      document.getElementsByTagName('head')[0].appendChild(node);
    }
  }

  loadMap() {
    const node = document.createElement('script');
    node.src =  '/assets/map.js';
    node.type = 'text/javascript';
    node.async = false;
    node.charset = 'utf-8';
    document.getElementsByTagName('body')[0].appendChild(node);
  }

  constructor() { }

  ngOnInit() {
    this.loadScripts();
    this.loadMap();
  }

}
