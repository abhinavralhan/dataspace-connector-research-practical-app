import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GraphDataService {

  constructor(private http: HttpClient) { }

  getHealthData(startDate: string, endDate: string): Observable<any> {
    const url = '/data/healthData?start_date=' + startDate + '&end_date=' + endDate;
    return this.http.get(url);
  }

  getHealthDatawithTime(startDatewithTime: string, endDatewithTime: string): Observable<any> {
    const url = '/data/healthData?start_date=' + startDatewithTime + '&end_date=' + endDatewithTime;
    return this.http.get(url);
  }


}
