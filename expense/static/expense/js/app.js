angular.module('managerapp', [ ])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller("expenseController",function($scope, $http){
    $scope.explist = {};
    $scope.ser = "";
    $scope.sum = function(obj, prop , initValue){
        var ret = initValue || 0;
        angular.forEach(obj, function(o){
            if (prop && o.hasOwnProperty(prop)) {
                ret = ret + o[prop];
            }
            else{
                ret = ret + obj;
            }
        });
        return ret;
    };
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
    $scope.delExpense = function(data, cb){
        if(data.hasOwnProperty('id')){
            url = '/expense/'+data.id;
            $http.delete(url)
                .success(function(response){
                    console.log("okay");
                    delete($scope.explist[data.id]);
                    if (!!cb)
                        cb(true);
                })
                .error(function(error){
                    console.log("data");
                    console.log(data);
                    console.log("Error");
                    console.log(error);
                    if (!!cb)
                        cb(false);
                })
            }

    }
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
        retrict:'A',
        scope : {
            ob:"=",
            updateParent:"&",
            deleteParent:"&"
        },
        controller:function($scope){
            $scope.deleting = false;
            $scope.toggleEdit = function(){
                $('#ob'+$scope.ob.id ).collapse('hide');
            };
            $scope.repost = function(edit){
                var dat = angular.copy($scope.ob);
                var cb = undefined;
                if(!!!edit){
                    delete(dat.id);
                }
                else{
                    cb = function(done){
                        if(done){
                            $scope.toggleEdit()
                        }
                    }
                }
                $scope.updateParent({d:dat, cb:cb});
            };
            $scope.pinIt = function(){
                dat = {'id':$scope.ob.id, 'pinned':! $scope.ob.pinned};
                $scope.updateParent({d:dat});
            };
            $scope.delete = function(){
                $scope.deleteParent({d:{id:$scope.ob.id}}) 
            }
        },
        templateUrl: ANGULAR_TEMPLATE_PATH +"expense/tmpl/exp_tmpl.html",
    };
});
