var app = angular.module('app');
app.directive('customChart', function(){
// var customChartDirective = function () {
	return {
    	restrict: 'E',
    	replace: true,
    	scope: {
    		key: '=',
    		dict: '='
    	},
        templateUrl: '/js/Directives/CustomChartDirective.html',
		controller: function($scope) {
			$scope.configs.push( {

                xAxis: {
                                categories: [$scope.dict[$scope.key]['categories']],
                                // categories: [new Date(1432691988000).toDateString(), new Date(1433281460000).toDateString(), new Date(1433282731000).toDateString(), new Date(1433330693000).toDateString(), new Date(1433332677000).toDateString()],
                },
                title: {
                    text: 'Temperature in Collegeville v. Blue Bell'
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
                    name: $scope.keys,
                    type:'area',
                    data: [$scope.dict[$scope.key]['temps']]
                }
                ]
            }
		}
	};

});

    


