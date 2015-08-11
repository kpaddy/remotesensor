var app = angular.module('app');
app.controller('ChartCtrl', function($scope, $http) {

    $http.get("/api?zipcode=19426")
        .success(function(data) {
            $scope.data = data;
            $scope.dict = {};
            for (var i = 0; i < $scope.data.length; i++) {
                if ($scope.dict.hasOwnProperty($scope.data[i].name) == false) {                     
                    $scope.dict[$scope.data[i].name] = {
                            categories: [],
                            temps: []
                        };
                };
                $scope.dict[$scope.data[i].name].categories.push($scope.data[i].dt * 1000);
                $scope.dict[$scope.data[i].name].temps.push($scope.data[i].otemp); 
            };          
            $scope.data2 = data;
            $scope.sensordata = {};
            for (var i = 0; i < $scope.data2.length; i++) {
                if ($scope.sensordata.hasOwnProperty($scope.data2[i].name) == false) {                     
                    $scope.sensordata[$scope.data2[i].name] = {
                            categories: [],
                            temps: []
                        };
                };
                $scope.sensordata[$scope.data2[i].name].categories.push($scope.data2[i].dt * 1000);
                $scope.sensordata[$scope.data2[i].name].temps.push($scope.data2[i].stemp); 
            };          
            
            $scope.configs =[];
            $scope.keys= Object.keys($scope.dict);
            for ($scope.key in $scope.keys) {
                $scope.categories = [];
                angular.forEach($scope.dict[$scope.keys[$scope.key]]['categories'], function(dateString){
                    dateString
                    var date = new Date(dateString)
                    $scope.categories.push(((date.getMonth()+1).toString().length ==1?'0'+(date.getMonth()+1).toString():(date.getMonth()+1).toString()) + '/' + ((date.getDate()).toString().length ==1?'0'+(date.getDate()).toString():(date.getDate()).toString())+ '/' + (date.getFullYear()) + ':' + date.getHours() + ' '+date.getMinutes());
                });
                $scope.configs.push ({
                    xAxis: {
                        categories:  $scope.categories , 
                        x: -20
                    },
                    title: {
                        text: 'Sensor Reading in ' + $scope.keys[$scope.key]
                    },            
                    yAxis:[ { 
                    	gridLineWidth: 0,
                        title: {
                            text: 'Outside',
                            style: {
                                color: Highcharts.getOptions().colors[0]
                            }
                        },
                        labels: {
                           format: '{value} C',
                            style: {
                                color: Highcharts.getOptions().colors[0]
                            }
                        }
                    }],                            
                    tooltip: { valueSuffix: ' celsius' },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'middle',
                        borderWidth: 0
                    },
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
                            name: $scope.keys[$scope.key],
                            type:'area',
                            data: $scope.dict[$scope.keys[$scope.key]]['temps']
                        },
                        {
                            name: $scope.keys[$scope.key],
                            type:'area',
                            data: $scope.sensordata["Evansburg"]['temps']
                        	
                        }
                    ]
                }) 
            };       
        })
        .error(function(data) {
            console.log('error');
        });
   
});