import {Component, OnInit} from '@angular/core';
import {LocalDataSource} from 'ng2-smart-table';
import {SmartTableData} from '../../@core/data/smart-table';
import {HomeService} from './home.service';
import {IMultiSelectOption, IMultiSelectSettings, IMultiSelectTexts} from 'angular-2-dropdown-multiselect';
import {Options} from 'ng5-slider';


@Component({
  selector: 'ngx-dashboard',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  tableSettings = HomeComponentConfiguration.tableSettings;
  tableDataSource = new LocalDataSource();
  tableData = [];

  algorithms = HomeComponentConfiguration.dataExplorationAlgorithms;
  selectedAlgorithm = 'Linear Regression';

  teams: string[];
  selectedTeams: string[];

  priceSliderOptions = HomeComponentConfiguration.priceSliderOptions;
  priceSliderBottom: number = 3;
  priceSliderUp: number = 14;

  formSliderOptions = HomeComponentConfiguration.formSliderOptions;
  formSliderBottom: number = 0;
  formSliderUp: number = 10;

  constructor(private service: SmartTableData, private homeService: HomeService) {
  }

  ngOnInit(): void {
    this.homeService.getTableData().subscribe(data => {
      this.tableData = data.table;
      this.tableDataSource.load(this.tableData);
      this.teams = data.teams;

      let bottomPrice = Math.max.apply(Math, data.table.map((row) => row.price));
      let upPrice = Math.min.apply(Math, data.table.map(row => row.price));
      this.priceSliderOptions.ceil = bottomPrice;
      this.priceSliderOptions.floor = upPrice;
      this.priceSliderBottom = bottomPrice;
      this.priceSliderUp = upPrice;

      let bottomForm = Math.max.apply(Math, data.table.map((row) => row.form));
      let upForm = Math.min.apply(Math, data.table.map(row => row.form));
      this.formSliderOptions.ceil = bottomForm;
      this.formSliderOptions.floor = upForm;
      this.formSliderBottom = bottomForm;
      this.formSliderUp = upForm;
    });
  }

  algorithmChange() {
    let algorithm = this.algorithms.find(algorithm => algorithm.name == this.selectedAlgorithm);
    this.homeService.getPredictionsByAlgorithm(algorithm.name).subscribe(predictions => {
      if (algorithm.type == 'regression') {
        this.tableData.forEach(row => {
          row.predictedPints = predictions[row.id];
        });
      } else {
        this.tableData.forEach(row => {
          row.predictedPints = HomeComponentConfiguration.pointsRanges[predictions[row.id]];
        });
      }
      this.tableDataSource.load(this.tableData);
    });
  }

  filterTableByName(playerName) {
    this.tableDataSource.addFilter({field: 'name', search: playerName});
  }

  filterTableByTeam() {
    if (this.selectedTeams) {
      this.tableDataSource.addFilter({
        field: 'team',
        search: this.selectedTeams,
        filter: (value, search) => {
          return search.some(team => team == value);
        }
      });
    } else {
      this.tableDataSource.addFilter({
        field: 'team',
        search: ''
      });
    }
  }

  filterTableByPrice() {
    this.tableDataSource.addFilter({
      field: 'price',
      search: [this.priceSliderBottom, this.priceSliderUp],
      filter: (value, search) => {
        return value >= search[0] && value <= search[1];
      }
    });
  }

  filterTableByForm() {
    this.tableDataSource.addFilter({
      field: 'form',
      search: [this.formSliderBottom, this.formSliderUp],
      filter: (value, search) => {
        return value >= search[0] && value <= search[1];
      }
    });
  }

  // test function connecting with backend
  testFunction(): void {
    this.homeService.testFunction().subscribe(test => {
      console.log(test);
    }, error => {
      console.log('error occured');
    });
  }

}

class HomeComponentConfiguration {

  public static dataExplorationAlgorithms = [
    {
      type: 'regression',
      name: 'Linear Regression'
    },
    {
      type: 'regression',
      name: 'SVM Regression'
    },
    {
      type: 'classification',
      name: 'SVM Classification'
    },
    {
      type: 'classification',
      name: 'Random Forest'
    },
    {
      type: 'classification',
      name: 'K-nearest neighbors'
    }
  ];

  public static priceSliderOptions: Options = {
    floor: 3,
    ceil: 14,
    step: 0.1
  };

  public static formSliderOptions: Options = {
    floor: 0,
    ceil: 10,
    step: 0.1
  };

  public static tableSettings = {
    actions: {
      add: false,
      edit: false,
      delete: false,
    },
    columns: {
      name: {
        title: 'Name',
      },
      team: {
        title: 'Team',
      },
      opponent: {
        title: 'Opponent',
      },
      price: {
        title: 'Price',
      },
      form: {
        title: 'Form',
      },
      predictedPints: {
        title: 'Predicted Points',
      },
    },
    hideSubHeader: true,
  };

  public static pointsRanges = {
    0: '0', 1: '1-2', 2: '3-6', 3: '>6'
  }
}
