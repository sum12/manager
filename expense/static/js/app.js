angular.module('managerapp',['ui.grid'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller('expense_ctrlr',function($scope, $http){
    $scope.gridOptions={};
   $http.get('/expense?format=json')
       .success(function(response){
           console.log(response.results);
           $scope.gridOptions.data=response.results;
       });
});
