import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MainComponent } from './main/main.component';
import {SystemRoutingModule} from "./system-routing.module";
import { CodeComponent } from './code/code.component';
import {CodemirrorModule} from "@ctrl/ngx-codemirror";
import {FormsModule} from "@angular/forms";
import { ProfileComponent } from './profile/profile.component';
import { ModelsComponent } from './models/models.component';
import { PortfolioComponent } from './portfolio/portfolio.component';
import { StategysComponent } from './stategys/stategys.component';
import { ExamplesComponent } from './examples/examples.component';
import { GraphComponent } from './graph/graph.component';
import { DocsComponent } from './docs/docs.component';


@NgModule({
  declarations: [
    MainComponent,
    CodeComponent,
    ProfileComponent,
    ModelsComponent,
    PortfolioComponent,
    StategysComponent,
    ExamplesComponent,
    GraphComponent,
    DocsComponent,
  ],
  imports: [
    CommonModule,
    SystemRoutingModule,
    CodemirrorModule,
    FormsModule
  ]
})
export class SystemModule { }
