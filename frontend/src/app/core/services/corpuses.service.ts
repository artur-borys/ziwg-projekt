import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CorpusesService {
  private api = environment.api;

  constructor(private http: HttpClient) { }

  getCorpuses(): Observable<{ data: string[] }> {
    return this.http.get<{ data: string[] }>(this.api + 'corpuses');
  }
}
