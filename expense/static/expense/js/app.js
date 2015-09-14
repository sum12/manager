angular.module('managerapp', [ ])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller("expenseController",function($scope, $http){
    $scope.explist = [];
    $scope.ser = "";
    $scope.parseDate = function(key){
        console.log(key)
       var x =  -parseInt(key.dateAdded.split('-').join(''));
       console.log(x);
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
                $scope.explist[i]['_id'] = i;
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
                .success(function(){
                    console.log("okay");
                    //console.log($scope.explist);
                    //console.log(data);
                    $scope.explist.splice(data._id,1);
                    if (!!cb)
                        cb(true);
                })
                .error(function(){
                    console.log("delete data Errored");
                    console.log(data);
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
                            response._id = data._id
                            $scope.explist[data._id] = response;
                            //console.log(response);
                            console.log("okay");
                            if (!!cb)
                                cb(true);
                        });
        }
        else{
            conn = $http.post(url,data)
                        .success(function(response){
                            response._id = $scope.explist.length;
                            $scope.explist.push(response)
                            //console.log(response);
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
                $scope.deleteParent({d:$scope.ob}) 
            }
        },
        templateUrl: ANGULAR_TEMPLATE_PATH +"expense/tmpl/exp_tmpl.html",
    };
});
