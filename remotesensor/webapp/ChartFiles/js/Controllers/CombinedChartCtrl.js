var app = angular.module('app');
app.controller('CombinedChartCtrl', function($scope, $http) {

    $http.get("/api?zipcode=19422")
        .success(function(data) {
            $scope.data = data;
            $scope.dict = {};
            for (var i = 0; i < $scope.data.rows.length; i++) {
                if ($scope.dict.hasOwnProperty($scope.data.rows[i].name) == false) {                     
                    $scope.dict[$scope.data.rows[i].name] = {
                            categories: [],
                            temps: []
                        };
                };
                $scope.dict[$scope.data.rows[i].name].categories.push($scope.data.rows[i]._id.dt * 1000);
                $scope.dict[$scope.data.rows[i].name].temps.push($scope.data.rows[i].main.temp); 
            };          
            $scope.keys= Object.keys($scope.dict);
            for ($scope.key in $scope.keys) {
                $scope.categories = [];
                angular.forEach($scope.dict[$scope.keys[$scope.key]]['categories'], function(dateString){
                    dateString
                    $scope.categories.push(new Date(dateString).toDateString());
                });
                $scope.temps = [];
                angular.forEach($scope.dict[$scope.keys[$scope.key]]['temps'], function(temp){
                    temp
                    $scope.temps.push(temp);
                });
            };
            console.log($scope.towns);
            console.log($scope.temps);
            console.log($scope.categories);
            $scope.configs = {
                xAxis: {
                    categories:  $scope.categories                            
                },
                title: {
                    text: 'Temperature in Collegeville and Blue Bell'
                },            
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' :
                        'Pinch the chart to zoom in'
                },
                yAxis: { title: { text: 'Temperature (Celsius)' } },
                tooltip: { valueSuffix: ' celsius' },
                legend: { align: 'center', verticalAlign: 'bottom', borderWidth: 0 },
                   plotOptions: {
                    area: {
                        fillColor: {
                            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                            stops: [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        },
                        marker: {
                            radius: 2
                        },
                        lineWidth: 1,
                        states: {
                            hover: {
                                lineWidth: 1
                            }
                        },
                        threshold: null
                    }
                },
                series: [
                    {
                        name: $scope.keys[0],
                        type:'area',
                        data: $scope.temps
                    },
                    {
                        name: $scope.keys[1],
                        type:'area',
                        data: $scope.temps
                    }
                ]
            }; 
                   
        })
        .error(function(data) {
            console.log('error');
        });
});