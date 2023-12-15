import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {SystemComponent} from "./system/system.component";
import {AuthGuard} from "./auth/auth.guard";
import {MainComponent} from "./system/main/main.component";
import {LoginComponent} from "./auth/login/login.component";
import {RegisterComponent} from "./auth/register/register.component";

const routes: Routes = [
  {
    path:'',component: SystemComponent,canActivate:[AuthGuard],children:[
      {path:'',component: MainComponent},
    ]
  },
  {
    path:'login',component:LoginComponent
  },
  {
    path:'register',component:RegisterComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
