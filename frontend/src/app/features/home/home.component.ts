import { Component, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { SimilarityService } from 'src/app/core/services/similarity.service';
import { StatementDto } from 'src/app/core/dtos/statement';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.sass'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent {

  isLoading: boolean = false;
  statements: StatementDto[] = [];

  form: FormGroup = new FormGroup({
    text: new FormControl(null, [Validators.required, Validators.maxLength(5000)]),
    method: new FormControl("tfidf"),
    corpus_variant: new FormControl("full"),
  })

  constructor(private similarityService: SimilarityService, private cdr: ChangeDetectorRef) { }

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
