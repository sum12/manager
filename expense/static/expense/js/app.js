angular.module('managerapp', [
        "xeditable"
        ])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller("expenseController",function($scope, $http){
    $scope.explist = {};
    $http.get('/expense')
        .success(function(response){
            $scope.explist = response.results;
            console.log("got the results");
            console.log($scope.explist);
        })
        .error(function(what){
            console.log(what);
        });
})
.directive("expense",function(){
    return{
        retrict : 'A',
        templateUrl: ANGULAR_TEMPLATE_PATH +"expense/tmpl/exp_tmpl.html"
    }
});
