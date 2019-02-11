import { NgModule } from '@angular/core';

import { ThemeModule } from '../../@theme/theme.module';
import { StylesRoutingModule, routedComponents } from './styles-routing.module';

@NgModule({
  imports: [
    StylesRoutingModule,
    ThemeModule,
  ],
  declarations: [
    ...routedComponents,
  ],
})
export class StylesModule { }
