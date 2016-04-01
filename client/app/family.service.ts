import {Injectable}     from 'angular2/core';
import {Http, Response, Headers, RequestOptions} from 'angular2/http';
import {Family}           from './family.interface';
import {Observable}     from 'rxjs/Observable';
import {Configuration} from './configuration';

@Injectable()
export class FamilyService {
    constructor(private http: Http, private config: Configuration) { }

    //private _familiesUrl = 'app/families.json';  // URL to web api
    
    private dbApi = btoa(this.config.dbApiUser+':'+this.config.dbApiPasswd);
    //private dbApi = btoa('neo4j:4demanog2');
    private _familiesUrl = this.config.dbApiUrl;
    //private _familiesUrl = 'http://localhost:7474/db/data/transaction/commit';
    
    getFamilies() {
        var headers = new Headers();
        headers.append('Accept', 'application/json');
        headers.append('Content-Type', 'application/json');
        headers.append('Authorization', 'Basic ' + this.dbApi);
        var params = '{"statements": [{ "statement":"match (f:Family) return f.name, f.description, f.since"}]}';
        return this.http.post(this.config.dbApiUrl, params, {headers:headers})
            .map(res => res.json().results[0].data)
            .catch(this.handleError);
    }

    private handleError(error: Response) {
        // in a real world app, we may send the error to some remote logging infrastructure
        // instead of just logging it to the console
        console.error(error);
        return Observable.throw(error.json() || 'Server error');
    }
}