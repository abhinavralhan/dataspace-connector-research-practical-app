import { AfterViewInit, Component, ViewEncapsulation, ViewChild, ChangeDetectorRef } from '@angular/core';
import { ChartConfiguration, ChartType, Chart } from 'chart.js';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { FormControl, FormGroup } from '@angular/forms';
import { GraphDataService } from '../graph-data.service';
import * as moment from 'moment';
import { AgreementViewService } from '../agreement-view/agreement-view.service';
import { DatePipe } from '@angular/common';
import { MatSnackBar } from '@angular/material/snack-bar';


export interface HealthData {
  eventTimestamp: Date;
  heartRate: number;
  systolicBP: number;
  diastolicBP: number;
  bodyTemperature: number;
  breathingFrequency: number;
  healthState: String;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  encapsulation: ViewEncapsulation.None
})

export class DashboardComponent implements AfterViewInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  public lineChartType: ChartType = 'line';
  range = new FormGroup({
    start: new FormControl<Date | null>(null),
    end: new FormControl<Date | null>(null),
  });
  displayedColumns: string[] = ['eventTimestamp', 'heartRate', 'systolicBP', 'diastolicBP', 'bodyTemperature', 'breathingFrequency', 'healthState'];
  source: HealthData[] = [];
  dataSource = new MatTableDataSource<HealthData>;
  countryData: Object = null;
  isLoaded: boolean = false;
  today = new Date();
  startDate: Date = this.today;
  endDate: Date = this.today;

  isEditing: boolean = false;

  element: String;
  startEditing(element: { isEditing: boolean; }) {
    element.isEditing = true;
  }

  showSnackbar(message: string) {
    this.snackBar.open(message, 'Dismiss', {
      duration: 3000
    });
  }


  datas: any = [
  ];
  public lineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: true,
    elements: {
      line: {
        tension: 0.5
      }
    },
    scales: {
      x: {},
      y:
      {
        position: 'left',
      },
      y1: {
        position: 'right',
        grid: {
          color: 'rgba(255,0,0,0.3)',
        },
        ticks: {
          color: 'red'
        }
      }
    },

    plugins: {
      legend: { display: true }
    }
  }
  public firstChartData: ChartConfiguration['data'] = { datasets: [] }
  hyperParams: any;
  showLoader: boolean;
  constructor(private snackBar: MatSnackBar, private api: GraphDataService, private changeDetectorRefs: ChangeDetectorRef, private _agreementViewService: AgreementViewService) {
    this.dataSource = new MatTableDataSource<HealthData>(this.source);
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  ngOnInit() {
    this.getChartData();
  }


  formatDate(date: Date) {
    var d = new Date(date),
      month = '' + (d.getMonth() + 1),
      day = '' + d.getDate(),
      year = d.getFullYear();

    if (month.length < 2)
      month = '0' + month;
    if (day.length < 2)
      day = '0' + day;

    return [year, month, day].join('-');
  }

  onSubmit() {
    this.getChartData();
  }

  getChartData() {
    this.api.getHealthData(this.formatDate(this.startDate), (this.formatDate(this.endDate))).subscribe(data => {
      this.datas = data;
      this.source = [];
      this.updateChart(data);
      this.datas.forEach((item: any) => {
        this.source.push({
          eventTimestamp: item.eventTimestamp, heartRate: item.vitals.heartRate, systolicBP: item.vitals.systolicBloodPressure,
          diastolicBP: item.vitals.diastolicBloodPressure, bodyTemperature: item.vitals.bodyTemperature,
          breathingFrequency: item.vitals.breathingFrequency, healthState: item.healthState
        });
      });
      this.dataSource = new MatTableDataSource<HealthData>(this.source);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      this.changeDetectorRefs.detectChanges();
    });

  }

  public updateChart(datas: any) {
    const newChartData = {
      // labels: datas.map((data: any)=> moment(data.eventTimestamp).format('MM/DD/YYYY')),
      labels: datas.map((data: any) => data.eventTimestamp),
      datasets: [
        {
          data: datas.map((data: any) => data.vitals.heartRate),
          label: 'Heart Rate'
        },
        {
          data: datas.map((data: any) => data.vitals.systolicBloodPressure),
          label: 'Systolic Blood Pressure'
        },
        {
          data: datas.map((data: any) => data.vitals.diastolicBloodPressure),
          label: 'Diastolic Blood Pressure'
        },
        {
          data: datas.map((data: any) => data.vitals.bodyTemperature),
          label: 'Body Temperature'
        },
        {
          data: datas.map((data: any) => data.vitals.breathingFrequency),
          label: 'Breathing Frequency'
        },
      ]
    };
    this.firstChartData = newChartData;
    this.isLoaded = true;
  }

  getLast15MinutesData() {
    const currentTime = new Date();
    const fifteenMinutesAgo = new Date(currentTime.getTime() - (15 * 60 * 1000)); // subtract 15 minutes in milliseconds

    const currentTimeFormatted = this.formatTime(currentTime);
    const fifteenMinutesAgoFormatted = this.formatTime(fifteenMinutesAgo);
    this.api.getHealthDatawithTime(fifteenMinutesAgoFormatted, currentTimeFormatted).subscribe(data => {
      this.datas = data;
      this.source = [];
      this.updateChart(data);
      this.datas.forEach((item: any) => {
        this.source.push({
          eventTimestamp: item.eventTimestamp, heartRate: item.vitals.heartRate, systolicBP: item.vitals.systolicBloodPressure,
          diastolicBP: item.vitals.diastolicBloodPressure, bodyTemperature: item.vitals.bodyTemperature,
          breathingFrequency: item.vitals.breathingFrequency, healthState: item.healthState
        });
      });
      this.dataSource = new MatTableDataSource<HealthData>(this.source);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      this.changeDetectorRefs.detectChanges();
    });
  }

  getLast1HourData() {
    const currentTime = new Date();
    const oneHourAgo = new Date(currentTime.getTime() - (60 * 60 * 1000));

    const currentTimeFormatted = this.formatTime(currentTime);
    const oneHourAgoFormatted = this.formatTime(oneHourAgo);

    this.api.getHealthDatawithTime(oneHourAgoFormatted, currentTimeFormatted).subscribe(data => {
      this.datas = data;
      this.source = [];
      this.updateChart(data);
      this.datas.forEach((item: any) => {
        this.source.push({
          eventTimestamp: item.eventTimestamp, heartRate: item.vitals.heartRate, systolicBP: item.vitals.systolicBloodPressure,
          diastolicBP: item.vitals.diastolicBloodPressure, bodyTemperature: item.vitals.bodyTemperature,
          breathingFrequency: item.vitals.breathingFrequency, healthState: item.healthState
        });
      });
      this.dataSource = new MatTableDataSource<HealthData>(this.source);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      this.changeDetectorRefs.detectChanges();
    });
  }

  formatTime(date: Date): string {
    const year = date.getUTCFullYear();
    const month = this.padZero(date.getUTCMonth() + 1);
    const day = this.padZero(date.getUTCDate());
    const hours = this.padZero(date.getUTCHours() + 1);
    const minutes = this.padZero(date.getUTCMinutes());
    const seconds = this.padZero(date.getUTCSeconds());
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}Z`;
  }

  padZero(value: number): string {
    return value < 10 ? `0${value}` : `${value}`;
  }

  getLast12HourData() {
    const currentTime = new Date();
    const twelveHourAgo = new Date(currentTime.getTime() - (60 * 12 * 60 * 1000));

    const currentTimeFormatted = this.formatTime(currentTime);
    const twelveHourAgoFormatted = this.formatTime(twelveHourAgo);

    this.api.getHealthDatawithTime(twelveHourAgoFormatted, currentTimeFormatted).subscribe(data => {
      this.datas = data;
      this.source = [];
      this.updateChart(data);
      this.datas.forEach((item: any) => {
        this.source.push({
          eventTimestamp: item.eventTimestamp, heartRate: item.vitals.heartRate, systolicBP: item.vitals.systolicBloodPressure,
          diastolicBP: item.vitals.diastolicBloodPressure, bodyTemperature: item.vitals.bodyTemperature,
          breathingFrequency: item.vitals.breathingFrequency, healthState: item.healthState
        });
      });
      this.dataSource = new MatTableDataSource<HealthData>(this.source);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      this.changeDetectorRefs.detectChanges();
    });
  }
  getLast48HoursData() {
    const currentTime = new Date();
    const fourtyeightHourAgo = new Date(currentTime.getTime() - (60 * 48 * 60 * 1000));

    const currentTimeFormatted = this.formatTime(currentTime);
    const twelveHourAgoFormatted = this.formatTime(fourtyeightHourAgo);

    this.api.getHealthDatawithTime(twelveHourAgoFormatted, currentTimeFormatted).subscribe(data => {
      this.datas = data;
      this.source = [];
      this.updateChart(data);
      this.datas.forEach((item: any) => {
        this.source.push({
          eventTimestamp: item.eventTimestamp, heartRate: item.vitals.heartRate, systolicBP: item.vitals.systolicBloodPressure,
          diastolicBP: item.vitals.diastolicBloodPressure, bodyTemperature: item.vitals.bodyTemperature,
          breathingFrequency: item.vitals.breathingFrequency, healthState: item.healthState
        });
      });
      this.dataSource = new MatTableDataSource<HealthData>(this.source);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      this.changeDetectorRefs.detectChanges();
    });
  }

  executeMlModel() {
    this.showLoader = true;
    this._agreementViewService.executeMlModel().subscribe(
      response => {
        this.showToast();
        this.showLoader = false;
      },
      error => {
        this.showLoader = false;
        //handle error here
      }
    );
  }

  triggerTraining() {
    this.showLoader = true;
    this._agreementViewService.triggerTraining().subscribe(
      response => {
        this.showToast();
        this.showLoader = false;
      },
      error => {
        this.showLoader = false;
        //handle error here
      }
    );
  }

  getHyperParams() {
    this.showLoader = true;
    this._agreementViewService.getHyperParams().subscribe(
      response => {
        this.showLoader = false;
        this.hyperParams = [response];
      },
      error => {
        this.showLoader = false;
        //handle error here
      }
    );
  }

  showToast() {
    const toaster = document.querySelector('.toaster');
    toaster.classList.add('active');
    setTimeout(function () {
      toaster.classList.remove('active');
    }, 3000);
  }


}
