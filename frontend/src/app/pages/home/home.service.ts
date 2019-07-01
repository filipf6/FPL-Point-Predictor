import {Injectable} from '@angular/core';
import {RestService} from '../../utils/rest.service';
import {Observable} from 'rxjs/Rx';
import {Test} from '../../models/test.model';
import {SmartTableData} from '../../@core/data/smart-table';
import {SmartTableService} from '../../@core/mock/smart-table.service';

@Injectable()
export class HomeService {
  constructor(private restService: RestService, private service: SmartTableService) {
  }

  testFunction(): Observable<Test> {
    return this.restService.get(`player-samples/test-url`);
  }

  getPredictionsByAlgorithm(algorithmName: string): Observable<any> {
    switch (algorithmName) {
      case 'Linear Regression':
        return Observable.of(this.service.getPredictedPoints().linearRegression);
      case 'SVM Regression':
        return Observable.of(this.service.getPredictedPoints().svmRegression);
      case 'SVM Classification':
        return Observable.of(this.service.getPredictedPoints().svmClassification);
      case 'Random Forest':
        return Observable.of(this.service.getPredictedPoints().randomForest);
      case 'K-nearest neighbors':
        return Observable.of(this.service.getPredictedPoints().kNearestNeighbors);
    }
  }


  getTableData(): Observable<any> {

    const data = {
      table: this.service.getData(),
      teams: [
        'Manchester City',
        'Manchester United',
        'Tottenham Hotspur',
        'Liverpool FC',
        'Chelsea London',
        'Arsenal',
        'Burnley',
        'Everton',
        'Leicester City',
        'Newcastle United',
        'Crystal Palace',
        'Bournemouth',
        'West Ham United',
        'Watford',
        'Brighton & Hove Albion',
        'Huddersfield Town',
        'Southampton',
        'Wolverhampton Wanderers',
        'Cardiff City',
        'Fulham',
      ]
    };
    return Observable.of(data);
  }
}
