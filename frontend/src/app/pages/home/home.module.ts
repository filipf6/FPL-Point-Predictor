import {NgModule} from '@angular/core';


import {ThemeModule} from '../../@theme/theme.module';
import {HomeComponent} from './home.component';
import {Ng2SmartTableModule} from 'ng2-smart-table';
import {MultiselectDropdownModule} from 'angular-2-dropdown-multiselect';
import {Ng5SliderModule} from 'ng5-slider';

@NgModule({
  imports: [
    ThemeModule,
    Ng2SmartTableModule,
    MultiselectDropdownModule,
    Ng5SliderModule,
  ],
  declarations: [
    HomeComponent,
  ],
})
export class HomeModule {
}
