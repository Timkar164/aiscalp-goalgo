import { Component, OnInit } from '@angular/core';
import {CodeService} from "../../servise/code.service";
import {Strategy} from "../../shared/models/strategy";

const defaults = {
  'text/x-python': 'def a(): \n' +
    ' pass'
};

@Component({
  selector: 'app-code',
  templateUrl: './code.component.html',
  styleUrls: ['./code.component.css']
})

export class CodeComponent {
  readOnly = false;
  content:any= '';
  mode: keyof typeof defaults = 'text/x-python';
  options = {
    lineNumbers: true,
    mode: this.mode,
  };
  defaults = defaults;
  errors:any = []
  data:any
  codemode: boolean = true;
  is_check: boolean = false;
  is_start: boolean = false;
  fileToUpload: File | null = null;
  envFileToUpload: File | null = null;
  strategy = new Strategy();

  constructor(private servise:CodeService) {
  }
  handleChange($event: Event): void {
    this.content = $event
  }

  handleFileInput(files: any) {
    this.fileToUpload = files.target.files.item(0);
    console.log(this.fileToUpload)
    let reader = new FileReader();

    reader.readAsText(files.target.files.item(0));
    reader.onload = (e)=>{
      this.content = reader.result
      this.ckeckCode()
    };

  }

  envhandleFileInput(files: any) {
    this.envFileToUpload = files.target.files.item(0);
  }

  cangeMode(){
    if (!this.codemode){
      this.is_check = false
      this.errors = []
    }
    this.codemode=!this.codemode

  }

  ckeckCode(){
    this.errors = []
    this.is_check = false
    this.servise.checkCode(this.content).subscribe(value => {
      this.data = value
      for(let i=0;i<this.data.items.length;i++){
        this.errors.push(this.data.items[i])
      }
      this.is_check = true
    })
  }

  start(){

  }

  clear(): void {
    this.defaults[this.mode] = '';
  }

  publishStrategy(){
    this.is_start = true;
    if(this.codemode){
    this.servise.runCode(this.envFileToUpload,this.fileToUpload,this.strategy).subscribe(value => {
      console.log(value)
    })}
    else{
      this.servise.runEditCode(this.envFileToUpload,this.content,this.strategy).subscribe(value=>{
        console.log(value)
      })
    }
  }
}
