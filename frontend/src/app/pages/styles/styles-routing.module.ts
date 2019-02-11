import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StylesComponent } from './styles.component';
import { LayoutsComponent } from './layouts/layouts.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { ThemesComponent } from './themes/themes.component';

const routes: Routes = [{
  path: '',
  component: StylesComponent,
  children: [{
    path: 'layouts',
    component: LayoutsComponent,
  }, {
    path: 'sidebar',
    component: SidebarComponent,
  }, {
    path: 'themes',
    component: ThemesComponent,
  }],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class StylesRoutingModule { }

export const routedComponents = [
  StylesComponent,
  LayoutsComponent,
  SidebarComponent,
  ThemesComponent,
];
