import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SystemComponent } from './system/system.component';
import {AuthGuard} from "./auth/auth.guard";
import {HttpClientModule} from "@angular/common/http";
import {AuthModule} from "./auth/auth.module";
import { HeaderComponent } from './shared/header/header.component';
import { MenuComponent } from './shared/menu/menu.component';
import {SystemModule} from "./system/system.module";

@NgModule({
  declarations: [
    AppComponent,
    SystemComponent,
    HeaderComponent,
    MenuComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    AuthModule,
    SystemModule
  ],
  providers: [AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
