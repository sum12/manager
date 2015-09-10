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
            res = response.results;
            for(i=0; i<res.length; i++){
                $scope.explist[res[i].id] = res[i];
            }
            console.log("Got the data");
        })
        .error(function(what){
            console.log('Fuck!!');
            console.log(what);
        });
    $scope.saveExpense = function(data, cb){
        url = "/expense";
        if (data.hasOwnProperty('id')){
            url += '/'+data.id;
            conn = $http.patch(url,data)
                        .success(function(response){
                            $scope.explist[data.id] = response;
                            console.log("okay");
                            if (!!cb)
                                cb(true);
                        });
        }
        else{
            conn = $http.post(url,data)
                        .success(function(response){
                            $scope.explist[response.id] = response;
                            console.log("okay");
                            if (!!cb)
                                cb(true);
                        });
        }
        conn.error(function(error){
                    console.log("data");
                    console.log(data);
                    console.log("Error");
                    console.log(error);
                    if (!!cb)
                        cb(false);
                })
    };
})
.directive("expense",function(){
    return{
        replace:true,
        retrict:'A',
        scope : {
            ob:"=",
            updateParent:"&"
        },
        controller:function($scope){
                $scope.toggleEdit = function(){
                    $scope.editing = !$scope.editing;
                };
                $scope.repost = function(edit){
                    var dat = angular.copy($scope.ob);
                    if(!!!edit){
                        delete(dat.id);
                    }
                    cb = function(done){
                        if(done){
                            $scope.toggleEdit()
                        }
                    }
                    $scope.updateParent({d:dat, cb:cb});
                };
                $scope.pinIt = function(){
                    dat = {'id':$scope.ob.id, 'pinned':! $scope.ob.pinned};
                    $scope.updateParent({d:dat});
                };
            },
        templateUrl: ANGULAR_TEMPLATE_PATH +"expense/tmpl/exp_tmpl.html",
    };
});
