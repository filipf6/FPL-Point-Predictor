import {Component} from '@angular/core';
import {LocalDataSource} from 'ng2-smart-table';
import {SmartTableData} from "../../@core/data/smart-table";
import {HomeService} from "./home.service";
import {IMultiSelectOption, IMultiSelectSettings, IMultiSelectTexts} from 'angular-2-dropdown-multiselect';
import {Options} from 'ng5-slider';


@Component({
  selector: 'ngx-dashboard',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  // predictions table configuration
  // TODO: move from component
  settings = {
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
  source: LocalDataSource = new LocalDataSource();


  // multiselect dropdown config
  // TODO: move from component
  optionsModel: string[];
  myOptions: IMultiSelectOption[];
  mySettings: IMultiSelectSettings = {
    //enableSearch: true,
    //checkedStyle: 'fontawesome',
    //buttonClasses: 'btn btn-default btn-hero-primary',
    //itemClasses: 'btn btn-default',
    //containerClasses: 'btn btn-default',
    dynamicTitleMaxItems: 3,
    displayAllSelectedText: true
  };
  myTexts: IMultiSelectTexts = {
    checkAll: 'Select all',
    uncheckAll: 'Unselect all',
    checked: 'item selected',
    checkedPlural: 'items selected',
    searchPlaceholder: 'Find',
    searchEmptyResult: 'Nothing found...',
    searchNoRenderText: 'Type in search box to see results...',
    defaultTitle: 'Team',
    allSelected: 'All selected',
  };

  // slider config
  // TODO: change to values coming from backend
  value: number = 3;
  highValue: number = 11;
  options: Options = {
    floor: 3,
    ceil: 14,
  };

  constructor(private service: SmartTableData, private homeService: HomeService) {

    // loading mocked data for table from smart-table.service.ts
    // TODO: change to loading from homeService
    const data = this.service.getData();
    this.source.load(data);

    // mocked data for teams multiple dropdown
    // TODO: change to loading from homeService
    this.myOptions = [
      {id: 1, name: 'Arsenal London'},
      {id: 2, name: 'Manchester City'},
      {id: 3, name: 'Chelsea London'},
      {id: 4, name: 'Manchester United'},
      {id: 5, name: 'Everton'},
      {id: 6, name: 'Liverpool FC'},
      {id: 7, name: 'Spurs'},
      {id: 8, name: 'Cardiff'},
    ];
  }

  // test function connecting with backend
  testFunction(): void {
    this.homeService.testFunction().subscribe(test => {
      console.log(test);
    }, error => {
      console.log('error occured');
    });
  }

  // function called on change of multiselect dropdown
  onChange() {
    console.log(this.optionsModel);
  }
}
