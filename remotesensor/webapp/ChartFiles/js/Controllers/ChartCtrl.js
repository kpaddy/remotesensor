var app = angular.module('app');
app.controller('ChartCtrl', function($scope, $http) {

    $http.get("/api?zipcode=19426")
        .success(function(data) {
            $scope.data = data.outside;
            $scope.dict = {};
            for (var i = 0; i < $scope.data.length; i++) {
                if ($scope.dict.hasOwnProperty($scope.data[i].name) == false) {                     
                    $scope.dict[$scope.data[i].name] = {
                            categories: [],
                            temps: []
                        };
                };
                $scope.dict[$scope.data[i].name].categories.push($scope.data[i]._id.dt * 1000);
                $scope.dict[$scope.data[i].name].temps.push($scope.data[i].main.temp); 
            };          
            $scope.data2 = data.sensor;
            $scope.sensordata = {};
            for (var i = 0; i < $scope.data2.length; i++) {
                if ($scope.sensordata.hasOwnProperty($scope.data2[i].sensorid) == false) {                     
                    $scope.sensordata[$scope.data2[i].sensorid] = {
                            categories: [],
                            temps: []
                        };
                };
                $scope.sensordata[$scope.data2[i].sensorid].categories.push($scope.data2[i].createdTime);
                $scope.sensordata[$scope.data2[i].sensorid].temps.push($scope.data2[i].temperature); 
            };          
            
            $scope.configs =[];
            $scope.keys= Object.keys($scope.dict);
            for ($scope.key in $scope.keys) {
                $scope.categories = [];
                angular.forEach($scope.dict[$scope.keys[$scope.key]]['categories'], function(dateString){
                    dateString
                    $scope.categories.push(new Date(dateString).toDateString());
                });
                $scope.configs.push ({
                    xAxis: {
                        categories:  $scope.categories                            
                    },
                    title: {
                        text: 'Temperature in ' + $scope.keys[$scope.key]
                    },            
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                            'Click and drag in the plot area to zoom in' :
                            'Pinch the chart to zoom in'
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
                    } ,  
                            { 
                        gridLineWidth: 0,
                        title: {
                            text: 'Sensor Reading',
                            style: {
                                color: Highcharts.getOptions().colors[1]
                            }
                        },
                        labels: {
                            format: '{value} C',
                            style: {
                                color: Highcharts.getOptions().colors[1]
                            }
                        }
                    }],
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
                            name: $scope.keys[$scope.key],
                            type:'area',
                            data: $scope.dict[$scope.keys[$scope.key]]['temps']
                        },
                        {
                            name: $scope.keys[$scope.key],
                            type:'area',
                            data: $scope.sensordata["1000"]['temps']
                        	
                        }
                    ]
                }) 
            };       
        })
        .error(function(data) {
            console.log('error');
        });
   
});