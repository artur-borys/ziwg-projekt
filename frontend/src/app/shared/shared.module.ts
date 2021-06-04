import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './components/header/header.component';
import { StatementComponent } from './components/statement/statement.component';
import { LoaderComponent } from './components/loader/loader.component';

const COMPONENTS = [
  HeaderComponent,
  StatementComponent,
  LoaderComponent
];

@NgModule({
  declarations: [
    COMPONENTS   
  ],
  imports: [
    CommonModule
  ],
  exports: [COMPONENTS]
})
export class SharedModule { }
