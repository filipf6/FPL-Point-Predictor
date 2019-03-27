import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs/Rx";

@Injectable()
export class RestService {

  constructor(private http: HttpClient) {
  }

  get(url: string): Observable<any> {
    return this.http.get('api/' + url);
  }
}
