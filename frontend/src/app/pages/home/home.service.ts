import {Injectable} from '@angular/core';
import {RestService} from '../../utils/rest.service';
import {Observable} from 'rxjs/Rx';
import {Test} from '../../models/test.model';

@Injectable()
export class HomeService {
  constructor(private restService: RestService) {
  }

  testFunction(): Observable<Test> {
    return this.restService.get(`player-samples/test-url`);
  }
}
