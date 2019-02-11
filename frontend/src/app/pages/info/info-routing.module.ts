import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { InfoComponent } from './info.component';
import { AboutComponent } from './about/about.component';

const routes: Routes = [{
  path: '',
  component: InfoComponent,
  children: [{
    path: 'about',
    component: AboutComponent,
  }],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class InfoRoutingModule { }

export const routedComponents = [
  InfoComponent,
  AboutComponent,
];
