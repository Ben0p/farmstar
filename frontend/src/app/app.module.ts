import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LayoutModule } from '@angular/cdk/layout';
import { HttpClientModule } from '@angular/common/http';
import { HttpModule } from '@angular/http';

// material imports
import { MaterialModule } from './material';

// components
import { AppComponent } from './app.component';
import { AppsComponent } from './apps/apps.component';
import { MapComponent } from './map/map.component';
import { LayersComponent } from './layers/layers.component';
import { ToolsComponent } from './tools/tools.component';
import { AboutComponent } from './about/about.component';
import { SettingsComponent } from './settings/settings.component';
import { ContactComponent } from './contact/contact.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MusicComponent } from './music/music.component';
import { AssignmentComponent } from './assignment/assignment.component';
import { CamerasComponent } from './cameras/cameras.component';
import { AdminComponent } from './admin/admin.component';
import { CommComponent } from './comm/comm.component';
import { NetworkComponent } from './network/network.component';
import { CalendarComponent } from './calendar/calendar.component';
import { KpiComponent } from './kpi/kpi.component';
import { DevicesComponent } from './devices/devices.component';


@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    LayersComponent,
    ToolsComponent,
    AboutComponent,
    AppsComponent,
    SettingsComponent,
    ContactComponent,
    DashboardComponent,
    MusicComponent,
    AssignmentComponent,
    CamerasComponent,
    AdminComponent,
    CommComponent,
    NetworkComponent,
    CalendarComponent,
    KpiComponent,
    DevicesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    LayoutModule,
    FlexLayoutModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})

export class AppModule {
}
