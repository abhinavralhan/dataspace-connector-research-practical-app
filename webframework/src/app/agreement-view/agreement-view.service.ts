import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

const baseUrl = "/data/";

@Injectable({
  providedIn: 'root'
})
export class AgreementViewService {

  constructor(private http: HttpClient) { }

  getAgreementList(): Observable <any> {
    //update get url here
    return this.http.get(baseUrl + "getAgreements");
  }

  executeMlModel(): Observable <any> {
    return this.http.get(baseUrl + "triggerDataSynthesizer");
  }

  triggerTraining(): Observable <any> {
    return this.http.get(baseUrl + "startTraining");
  }

  getHyperParams(): Observable <any> {
    return this.http.get(baseUrl + "getHyperparameters");
  }


  mockHyperParams (): Observable <any>{
    const response = [{
          "max_depth": 9.0,
          "random_state": 15.0,
          "min_samples_split": 2.0
      },
      {
        "max_depth": 9.0,
        "random_state": 15.0,
        "min_samples_split": 2.0
    },
    {
      "max_depth": 9.0,
      "random_state": 15.0,
      "min_samples_split": 2.0
    }
];

    let obs = new Observable((subscriber) => {
        setTimeout(()=>{
            subscriber.next(response);
            subscriber.complete();
        }, 3000);
    });
    return obs;
  }
}
