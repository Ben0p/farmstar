import { NgModule } from '@angular/core';

import { ThemeModule } from '../../@theme/theme.module';
import { InfoRoutingModule, routedComponents } from './info-routing.module';

@NgModule({
  imports: [
    ThemeModule,
    InfoRoutingModule,
  ],
  exports: [],
  declarations: [
    ...routedComponents,
  ],
})
export class InfoModule { }
