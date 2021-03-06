import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { StatementDto } from '../dtos/statement';

@Injectable({
  providedIn: 'root'
})
export class SimilarityService {
  private api = environment.api;

  constructor(private http: HttpClient) { }

  getSimilarity(data: { text: string, method: string, corpus_variant: string, corpus_name: string }): Observable<StatementDto[]> {
    return this.http.post<StatementDto[]>(this.api + 'similarity', data);
  }
}
