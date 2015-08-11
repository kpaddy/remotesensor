'use strict';

app.controller('sensorCtrl', ['$scope','sensorService', function ($scope,sensorService) {
	$scope.msgtxt='';
	$scope.login=function(data, $scope){
		var $weatherData = sensorService.getWeather(data,$scope); //call service
		$scope.city = "King of Prussia";
		$scope.currentTemp = $weatherData[0];
		$scope.minTemp = $weatherData[1];
		$scope.maxTemp = $weatherData[2];
	};
}]);