import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AuthGuard} from "../auth/auth.guard";
import {MainComponent} from "./main/main.component";
import {SystemComponent} from "./system.component";
import {CodeComponent} from "./code/code.component";
import {ProfileComponent} from "./profile/profile.component";
import {PortfolioComponent} from "./portfolio/portfolio.component";
import {StategysComponent} from "./stategys/stategys.component";
import {ModelsComponent} from "./models/models.component";
import {ExamplesComponent} from "./examples/examples.component";
import {GraphComponent} from "./graph/graph.component";
import {DocsComponent} from "./docs/docs.component";

const routes: Routes = [
  {
    path:'',component: SystemComponent,canActivate:[AuthGuard],children:[
      {path:'',component: MainComponent},
      {path:'code',component: CodeComponent},
      {path:'profile',component:ProfileComponent},
      {path:'portfolio',component:PortfolioComponent},
      {path:'strategys',component:StategysComponent},
      {path:'models',component:ModelsComponent},
      {path:'examples',component:ExamplesComponent},
      {path:'docs',component:DocsComponent},
      {path:'graph',component:GraphComponent},
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class SystemRoutingModule{ }
