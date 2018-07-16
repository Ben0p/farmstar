import { Component, OnInit, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-layers',
  templateUrl: './layers.component.html',
  styleUrls: ['./layers.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class LayersComponent implements OnInit {

  panelOpenState = false;
  baseLayer: string;
  layers: string[] = [
    'satellite-v9',
    'satellite-streets-v10',
    'streets-v10',
    'outdoors-v10',
    'light-v9',
    'dark-v9'];
  terrains: string[] = [
    'landcover',
    'hillshade',
    'contour'
  ];
  markers: string[] = [
    'you',
    'vehicles',
    'obsticles'
  ];
  tracks: string[] = [
    'you',
    'vehicles',
    'kangaroos'
  ];
  networks: string[] = [
    'vehicles',
    'repeaters',
    'links'
  ];
  fields: string[] = [
    'This Field',
    'Other Field',
    'Next Feild'
  ];
  operations: string[] = [
    'Sprayed',
    'Harvested',
    'Seeded'
  ];

  constructor() { }

  ngOnInit() {
  }

}
