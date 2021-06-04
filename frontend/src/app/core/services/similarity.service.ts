import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { StatementDto } from '../dtos/statement';

@Injectable({
  providedIn: 'root'
})
export class SimilarityService {

  constructor(private http: HttpClient) { }

  getSimilarity(data: { text: string, method: string, corpus_variant: string }): Observable<StatementDto[]> {
    return this.http.post<StatementDto[]>('http://localhost:8080/similarity', data);
  }
}
