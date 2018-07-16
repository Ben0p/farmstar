import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Component imports
import { AboutComponent } from './about/about.component';
import { LayersComponent } from './layers/layers.component';
import { MapComponent } from './map/map.component';
import { ToolsComponent } from './tools/tools.component';
import { AppsComponent } from './apps/apps.component';
import { SettingsComponent } from './settings/settings.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ContactComponent } from './contact/contact.component';
import { MusicComponent } from './music/music.component';
import { AssignmentComponent } from './assignment/assignment.component';
import { CamerasComponent } from './cameras/cameras.component';
import { AdminComponent } from './admin/admin.component';
import { CommComponent } from './comm/comm.component';
import { CalendarComponent } from './calendar/calendar.component';
import { NetworkComponent } from './network/network.component';
import { KpiComponent } from './kpi/kpi.component';
import { DevicesComponent } from './devices/devices.component';



const routes: Routes = [
  {
    path: 'apps',
    component: AppsComponent
  },
  {
    path: 'map',
    component: MapComponent
  },
  {
    path: 'about',
    component: AboutComponent
  },
  {
    path: 'layers',
    component: LayersComponent
  },
  {
    path: 'tools',
    component: ToolsComponent
  },
  {
    path: 'settings',
    component: SettingsComponent
  },
  {
    path: 'dashboard',
    component: DashboardComponent
  },
  {
    path: 'contact',
    component: ContactComponent
  },
  {
    path: 'assignment',
    component: AssignmentComponent
  },
  {
    path: 'music',
    component: MusicComponent
  },
  {
    path: 'cameras',
    component: CamerasComponent
  },
  {
    path: 'admin',
    component: AdminComponent
  },
  {
    path: 'comm',
    component: CommComponent
  },
  {
    path: 'calendar',
    component: CalendarComponent
  },
  {
    path: 'network',
    component: NetworkComponent
  },
  {
    path: 'kpi',
    component: KpiComponent
  },
  {
    path: 'devices',
    component: DevicesComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
