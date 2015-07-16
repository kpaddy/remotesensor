var app = angular.module('app');
app.directive('chart', function(){
    return {
        restrict: 'E',
        replace: true,
        template: '<div></div>',
        scope: {
            config: '='
        },
        link: function (scope, element, attrs) {
            var chart;
            var process = function () {
                var defaultOptions = {
                    chart: { renderTo: element[0] },
                };
                var config = angular.extend(defaultOptions, scope.config);
                chart = new Highcharts.Chart(config);
            };
            process();
            scope.$watch("config.series", function (loading) {
                process();
            });
            scope.$watch("config.loading", function (loading) {
                debugger;
                if (!chart) {
                    return;
                }
                if (loading) {
                    chart.showLoading();
                } else {
                    chart.hideLoading();
                }
            });
        }
    };
});

