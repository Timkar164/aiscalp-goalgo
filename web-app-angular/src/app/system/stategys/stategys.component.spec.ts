import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StategysComponent } from './stategys.component';

describe('StategysComponent', () => {
  let component: StategysComponent;
  let fixture: ComponentFixture<StategysComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StategysComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StategysComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
