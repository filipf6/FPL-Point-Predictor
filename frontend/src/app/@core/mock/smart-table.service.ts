import {Injectable} from '@angular/core';
import {SmartTableData} from '../data/smart-table';

@Injectable()
export class SmartTableService extends SmartTableData {

  predictedPoints = {
    linearRegression:
      {
        1: 1.1,
        2: 2,
        3: 4.6,
        4: 0,
        5: 1,
        6: 1,
        7: 2,
        8: 3,
        9: 0.5,
        10: 1,
        11: 1.4,
        12: 2.9,
        13: 1.2,
        14: 1.9,
        15: 1.8,
        16: 3.8,
        17: 3.3,
        18: 2.9,
        19: 1.2,
        20: 3.0
      },
    svmRegression:
      {
        1: 0,
        2: 2,
        3: 3.9,
        4: 0,
        5: 1.1,
        6: 1,
        7: 2.2,
        8: 0.4,
        9: 0,
        10: 0,
        11: 1.6,
        12: 2.3,
        13: 1.1,
        14: 1.1,
        15: 1.4,
        16: 4.9,
        17: 3.0,
        18: 1.3,
        19: 1.2,
        20: 2.5
      },
    svmClassification:
      {1: 1, 2: 1, 3: 1, 4: 0, 5: 1, 6: 1, 7: 1, 8: 0, 9: 0, 10: 1, 11: 1, 12: 2, 13: 1, 14: 1, 15: 1, 16: 2, 17: 2, 18: 1, 19: 1, 20: 1},
    randomForest:
      {1: 1, 2: 2, 3: 2, 4: 0, 5: 1, 6: 1, 7: 1, 8: 0, 9: 1, 10: 0, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 2, 17: 1, 18: 1, 19: 1, 20: 1},
    kNearestNeighbors:
      {1: 1, 2: 2, 3: 3, 4: 0, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0, 10: 0, 11: 1, 12: 2, 13: 1, 14: 1, 15: 1, 16: 2, 17: 2, 18: 1, 19: 1, 20: 1},
  };


  data = [{
    id: 1,
    name: 'Alexis Sanchez',
    team: 'Manchester United',
    opponent: 'Liverpool FC',
    price: 11.3,
    form: 0.5,
    predictedPints: '0',
  }, {
    id: 2,
    name: 'Leroy Sane',
    team: 'Manchester City',
    opponent: 'Arsenal London',
    price: 10.0,
    form: 4.2,
    predictedPints: '1-2',
  }, {
    id: 3,
    name: 'Kepa',
    team: 'Chelsea London',
    opponent: 'Brighton',
    price: 5.5,
    form: 5.2,
    predictedPints: '3-6',
  }, {
    id: 4,
    name: 'Lewis Dunk',
    team: 'Brighton',
    opponent: 'Chelsea London',
    price: 4.6,
    form: 4.7,
    predictedPints: '1-2',
  }, {
    id: 5,
    name: 'Rob Green',
    team: 'Chelsea London',
    opponent: 'Brighton',
    price: 4.4,
    form: 0.3,
    predictedPints: '0',
  }, {
    id: 6,
    name: 'Mathew Ryan',
    team: 'Brighton',
    opponent: 'Chelsea London',
    price: 4.2,
    form: 3.4,
    predictedPints: '1-2',
  }, {
    id: 7,
    name: 'Antonio Rudiger',
    team: 'Chelsea London',
    opponent: 'Brighton',
    price: 5.3,
    form: 3.8,
    predictedPints: '3-6',
  }, {
    id: 8,
    name: 'Jiri Skalak',
    team: 'Brighton',
    opponent: 'Chelsea London',
    price: 4.0,
    form: 0.0,
    predictedPints: '0',
  }, {
    id: 9,
    name: 'Kurt Zouma',
    team: 'Chelsea London',
    opponent: 'Brighton',
    price: 5.3,
    form: 3.0,
    predictedPints: '1-2',
  }, {
    id: 10,
    name: 'Leonardo Ulloa',
    team: 'Brighton',
    opponent: 'Chelsea London',
    price: 3.9,
    form: 0.0,
    predictedPints: '0',
  },
    {
      id: 11,
      name: 'Fabianski',
      team: 'West Ham United',
      opponent: 'Leicester City',
      price: 5.0,
      form: 2.5,
      predictedPints: '0',
    }, {
      id: 12,
      name: 'Felipe Anderson',
      team: 'West Ham United',
      opponent: 'Leicester City',
      price: 7,
      form: 4.2,
      predictedPints: '1-2',
    }, {
      id: 13,
      name: 'Evans',
      team: 'Leicester City',
      opponent: 'West Ham United',
      price: 5.5,
      form: 1.2,
      predictedPints: '1-2',
    }, {
      id: 14,
      name: 'Chilwell',
      team: 'Leicester City',
      opponent: 'West Ham United',
      price: 4.6,
      form: '0.7',
      predictedPints: '1-2',
    }, {
      id: 15,
      name: 'Barnes',
      team: 'Leicester City',
      opponent: 'West Ham United',
      price: 4.4,
      form: '0.3',
      predictedPints: '1-2',
    }, {
      id: 16,
      name: 'Vardy',
      team: 'Leicester City',
      opponent: 'West Ham United',
      price: 7.5,
      form: 3.4,
      predictedPints: '3-6',
    }, {
      id: 17,
      name: 'Maddison',
      team: 'Leicester City',
      opponent: 'West Ham United',
      price: 7.0,
      form: 3.8,
      predictedPints: '3-6',
    }, {
      id: 18,
      name: 'Maguire',
      team: 'Leicester City',
      opponent: 'West Ham United',
      price: 5.0,
      form: 3.0,
      predictedPints: '1-2',
    }, {
      id: 19,
      name: 'Pereira',
      team: 'Leicester City',
      opponent: 'West Ham United',
      price: 5.5,
      form: 3.0,
      predictedPints: '1-2',
    }, {
      id: 20,
      name: 'Kasper Schmeichel',
      team: 'Leicester City',
      opponent: 'West Ham United',
      price: 5.0,
      form: 4.0,
      predictedPints: '0',
    },
  ];

  getPredictedPoints() {
    return this.predictedPoints;
  }

  getData() {
    const table = this.data;
    table.forEach(row => row.predictedPints = this.predictedPoints.linearRegression[row.id]);
    return table;
  }
}
