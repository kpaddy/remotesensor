'use strict';
app.factory('sensorService',function($http, $location){
	return{
		getWeather:function(data,scope){
			return [30, 22, 34]; 
			}
		}
});