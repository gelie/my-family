import {Injectable} from 'angular2/core';

@Injectable()

export class Configuration{
  public dbApiUrl: string = 'http://localhost:7474/db/data/transaction/commit';
  public dbApiUser: string = 'neo4j';
  public dbApiPasswd: string = '4demanog2';
}
