'use strict';

app.controller('homeCtrl', ['$scope','loginService', function($scope,loginService){
	$scope.txt='Welcome to your Temperature Sensor Homepage!';
	$scope.logout=function(){
		loginService.logout();
	}
}])