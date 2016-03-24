System.register(['angular2/core', 'angular2/http', 'rxjs/Observable', './configuration'], function(exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
        var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
        if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
        else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
        return c > 3 && r && Object.defineProperty(target, key, r), r;
    };
    var __metadata = (this && this.__metadata) || function (k, v) {
        if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
    };
    var core_1, http_1, Observable_1, configuration_1;
    var FamilyService;
    return {
        setters:[
            function (core_1_1) {
                core_1 = core_1_1;
            },
            function (http_1_1) {
                http_1 = http_1_1;
            },
            function (Observable_1_1) {
                Observable_1 = Observable_1_1;
            },
            function (configuration_1_1) {
                configuration_1 = configuration_1_1;
            }],
        execute: function() {
            FamilyService = (function () {
                function FamilyService(http, config) {
                    this.http = http;
                    this.config = config;
                    //private _familiesUrl = 'app/families.json';  // URL to web api
                    this.dbApi = btoa(this.config.dbApiUser + ':' + this.config.dbApiPasswd);
                    //private dbApi = btoa('neo4j:4demanog2');
                    this._familiesUrl = this.config.dbApiUrl;
                }
                //private _familiesUrl = 'http://localhost:7474/db/data/transaction/commit';
                FamilyService.prototype.getFamilies = function () {
                    var headers = new http_1.Headers();
                    headers.append('Accept', 'application/json');
                    headers.append('Content-Type', 'application/json');
                    headers.append('Authorization', 'Basic ' + this.dbApi);
                    var params = '{"statements": [{ "statement":"match (f:Family) return f.name, f.description, f.since"}]}';
                    return this.http.post(this.config.dbApiUrl, params, { headers: headers })
                        .map(function (res) { return res.json().results[0].data; })
                        .catch(this.handleError);
                };
                FamilyService.prototype.handleError = function (error) {
                    // in a real world app, we may send the error to some remote logging infrastructure
                    // instead of just logging it to the console
                    console.error(error);
                    return Observable_1.Observable.throw(error.json() || 'Server error');
                };
                FamilyService = __decorate([
                    core_1.Injectable(), 
                    __metadata('design:paramtypes', [http_1.Http, configuration_1.Configuration])
                ], FamilyService);
                return FamilyService;
            }());
            exports_1("FamilyService", FamilyService);
        }
    }
});
//# sourceMappingURL=family.service.js.map