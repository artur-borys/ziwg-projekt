import { Component, ChangeDetectionStrategy, ChangeDetectorRef, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { SimilarityService } from 'src/app/core/services/similarity.service';
import { StatementDto } from 'src/app/core/dtos/statement';
import { map } from 'rxjs/operators';
import { CorpusesService } from 'src/app/core/services/corpuses.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.sass'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent implements OnInit {

  isLoading: boolean = false;
  statements: StatementDto[] = [];
  corpuses$: Observable<string[]>;

  form: FormGroup = new FormGroup({
    text: new FormControl(null, [Validators.required, Validators.maxLength(5000)]),
    method: new FormControl("tfidf", [Validators.required]),
    corpus_variant: new FormControl("full", [Validators.required]),
    corpus_name: new FormControl("wypowiedzi_politykow", [Validators.required])
  })

  constructor(private similarityService: SimilarityService, private corpusesService: CorpusesService, private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    this.corpuses$ = this.corpusesService.getCorpuses().pipe(map((res) => res.data));
  }

  submit() {
    this.isLoading = true;
    this.statements = [];
    this.similarityService
      .getSimilarity(this.form.value)
      .pipe(map(res => res.slice(0, 10)))
      .subscribe((results) => {
        this.isLoading = false;
        this.statements = results;
        this.cdr.markForCheck();
      }, () => {
        this.isLoading = false;
        this.cdr.markForCheck();
      })
  }

}
