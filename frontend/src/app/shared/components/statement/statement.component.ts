import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { StatementDto } from 'src/app/core/dtos/statement';

@Component({
  selector: 'app-statement',
  templateUrl: './statement.component.html',
  styleUrls: ['./statement.component.sass'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class StatementComponent {

  @Input() statement: StatementDto;

  getColor(score) {
    if (score > 0.50) {
      return 'green';
    } else if (score > 0.25) {
      return 'yellow';
    } else {
      return 'red';
    }
  }

}
