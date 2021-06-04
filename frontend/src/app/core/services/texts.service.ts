import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { TextDto } from '../dtos/text';

@Injectable({
  providedIn: 'root'
})
export class TextsService {
  private api = environment.api;

  constructor(private http: HttpClient) { }

  getText(id: number, corpus_name: string): Observable<TextDto[]> {
    return this.http.get<TextDto[]>(this.api + `text/${id}?corpus_name=${corpus_name}`);
  }
}
