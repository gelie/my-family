System.register(['angular2/core', './family.service', 'angular2/common', './configuration'], function(exports_1, context_1) {
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
    var core_1, family_service_1, common_1, configuration_1;
    var FamilyList;
    return {
        setters:[
            function (core_1_1) {
                core_1 = core_1_1;
            },
            function (family_service_1_1) {
                family_service_1 = family_service_1_1;
            },
            function (common_1_1) {
                common_1 = common_1_1;
            },
            function (configuration_1_1) {
                configuration_1 = configuration_1_1;
            }],
        execute: function() {
            FamilyList = (function () {
                //families = ['fam1', 'fam2', 'fam3'];
                function FamilyList(_famService) {
                    this._famService = _famService;
                }
                FamilyList.prototype.ngOnInit = function () { this.getFamilies(); };
                FamilyList.prototype.getFamilies = function () {
                    var _this = this;
                    this._famService.getFamilies()
                        .subscribe(function (families) { return _this.families = families; }, function (error) { return _this.errorMessage = error; });
                };
                FamilyList = __decorate([
                    core_1.Component({
                        selector: 'family-list',
                        templateUrl: 'app/family-list.html',
                        providers: [family_service_1.FamilyService, configuration_1.Configuration],
                        directives: [common_1.CORE_DIRECTIVES]
                    }), 
                    __metadata('design:paramtypes', [family_service_1.FamilyService])
                ], FamilyList);
                return FamilyList;
            }());
            exports_1("FamilyList", FamilyList);
        }
    }
});
//# sourceMappingURL=family-list.component.js.map