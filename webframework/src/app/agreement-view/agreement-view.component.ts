import { Component, OnInit } from '@angular/core';
import { AgreementViewService } from './agreement-view.service';

@Component({
  selector: 'app-agreement-view',
  templateUrl: './agreement-view.component.html',
  styleUrls: ['./agreement-view.component.scss']
})
export class AgreementViewComponent implements OnInit {

  agreementList: any;

  constructor(private _agreementViewService: AgreementViewService) { }

  ngOnInit(): void {
    this.getAgreementList();
  }
  getAgreementList() {
    this._agreementViewService.getAgreementList().subscribe(
      response => {
       this.agreementList = response;
      },
      error => {
        //handle error here
      }
    );
  }

}


