import { Component, OnInit } from '@angular/core';

export interface Section {
  name: string;
  detail: string;
  icon: string;
}

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.scss']
})
export class DevicesComponent implements OnInit {

  gpss: Section[] = [
    {
      name: 'GPS 1',
      detail: 'Fixed',
      icon: 'gps_fixed',
    },
    {
      name: 'GPS 2',
      detail: 'None',
      icon: 'gps_off',
    }
  ];
  screens: Section[] = [
    {
      name: 'Battery',
      detail: '100%',
      icon: 'battery_charging_full',
    },
    {
      name: 'Main Storage',
      detail: '68%',
      icon: 'sd_storage',
    },
    {
      name: 'WiFi',
      detail: '-63dBm',
      icon: 'signal_wifi_4_bar',
    },
    {
      name: 'Bluetooth',
      detail: 'Paired',
      icon: 'bluetooth',
    }
  ];
  sensors: Section[] = [
    {
      name: 'Temperature',
      detail: '24°C',
      icon: '../../assets/icons/temperature.png',
    },
    {
      name: 'Humidity',
      detail: '84%',
      icon: '../../assets/icons/humidity.png',
    },
    {
      name: 'Pressure',
      detail: '1018.66hPa',
      icon: '../../assets/icons/pressure.png',
    },
    {
      name: 'Accelerometer',
      detail: 'x:-0.21 y:0.53 z:9.71 m/s²',
      icon: '../../assets/icons/accelerometer.png',
    },
    {
      name: 'Gyroscope',
      detail: 'x:-0.03 y:0.01 z:0.06 rad/s',
      icon: '../../assets/icons/gyroscope.png',
    },
  ];
  tyres: Section[] = [
    {
      name: 'Front Left',
      detail: '38.1 PSI',
      icon: '../../assets/icons/tyre_pressure.png',
    },
    {
      name: 'Front Right',
      detail: '37.8 PSI',
      icon: '../../assets/icons/tyre_pressure.png',
    },
    {
      name: 'Rear Left Outer',
      detail: '38.4 PSI',
      icon: '../../assets/icons/tyre_pressure.png',
    },
    {
      name: 'Rear Left Inner',
      detail: '38.2 PSI',
      icon: '../../assets/icons/tyre_pressure.png',
    },
    {
      name: 'Rear Right Outer',
      detail: '38.1 PSI',
      icon: '../../assets/icons/tyre_pressure.png',
    },
    {
      name: 'Rear Right Inner',
      detail: '37.9 PSI',
      icon: '../../assets/icons/tyre_pressure.png',
    },
  ];


  constructor() { }

  ngOnInit() {
  }

}
