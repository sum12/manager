angular.module('managerapp', [ ])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller("expenseController",function($scope, $http){
    $scope.explist = [];
    $scope.ser = "";
    $scope.parseDate = function(key){
       var x =  -parseInt(key.dateAdded.split('-').join(''));
       return x;
    };
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
                //$scope.explist[res[i].id] = res[i];
                $scope.explist.push(res[i])
            }
            console.log("Got the data");
        })
        .error(function(what){
            console.log('Fuck!!');
            console.log(what);
        });
    $scope.delExpense = function(data, cb){
        $scope.doing = true;
        console.log(data);
        if(data.hasOwnProperty('id')){
            url = '/expense/'+data.id;
            console.log("making delete requeset");
            $http.delete(url)
                .success(function(){
                    console.log("okay");
                    //console.log($scope.explist);
                    //console.log(data);
                    $scope.explist.splice($scope.explist.indexOf(data),1);
                    if (!!cb)
                        cb(true);
                    $scope.doing = false;
                })
                .error(function(){
                    console.log("delete data Errored");
                    console.log(data);
                    if (!!cb)
                        cb(false);
                    $scope.doing = false;
                })
            }
        else{
            console.log("unable to delete, Id not found");
        }
    }
    $scope.saveExpense = function(data, cb){
        url = "/expense";
        $scope.doing = true;
        if (data.hasOwnProperty('id')){
            url += '/'+data.id;
            conn = $http.patch(url,data)
                        .success(function(response){
                            $scope.explist[$scope.explist.indexOf(data)] = response;
                            console.log(response);
                            console.log("okay");
                            if (!!cb)
                                cb(true);
                        $scope.doing = false;
                        });
        }
        else{
            conn = $http.post(url,data)
                        .success(function(response){
                            $scope.explist.push(response)
                            //console.log(response);
                            console.log("okay");
                            if (!!cb)
                                cb(true);
                        $scope.doing = false;
                        });
        }
        conn.error(function(error){
                    console.log("data");
                    console.log(data);
                    console.log("Error");
                    console.log(error);
                    if (!!cb)
                        cb(false);
                    $scope.doing = false;
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
                var dat = $scope.ob;
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
                console.log("sending data for delete");
                console.log($scope.ob);
                $scope.deleteParent({d:$scope.ob}) 
            }
        },
        templateUrl: ANGULAR_TEMPLATE_PATH +"expense/tmpl/exp_tmpl.html",
    };
});
