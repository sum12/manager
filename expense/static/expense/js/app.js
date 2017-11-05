angular.module('managerapp', [ 'ui.bootstrap'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller("expenseController",function($scope, $http){
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
    var currentDate = new Date();
    if(!YEAR) YEAR = currentDate.getFullYear();
    if(!MONTH) MONTH = currentDate.getMonth();
    if(!DAY) DAY = 1//currentDate.getDate();
    $scope.pagedate = new Date(YEAR, MONTH , DAY)

    $scope.reload = function(){
        $scope.explist = [];
        $scope.taglist = [];
        $scope.alerts = [];
        $scope.doing = true;
        $http.get('/expenses/'+ $scope.pagedate.getFullYear() +'/'+ parseInt($scope.pagedate.getMonth()+1))
            .success(function(response){
                res = response;
                $scope.explist = []
                for(i=0; i<res.length; i++){
                    //$scope.explist[res[i].id] = res[i];
                    res[i].objdateAdded = new Date(res[i].dateAdded)
                    $scope.explist.push(res[i]);
                    splitTags=res[i].tag.split(',');
                    res[i].tags=splitTags;
                    angular.forEach(splitTags, function(value){
                        if ($scope.taglist.indexOf(value) == -1){
                            $scope.taglist.push(value)
                        }
                    });
                }
                //console.log($scope.taglist);
                $scope.doing = false;
                $scope.alerts.push({'type':'success', 'msg':'Got It!!'})
                console.log("Got the data");
            })
            .error(function(what){
                console.log('Fuck!!');
                console.log(what);
                $scope.doing = false;
            });
    };
    $scope.additionalTags = function(){
        var year = $scope.pagedate.getFullYear(),
            month = $scope.pagedate.getMonth();
        if ($scope.pagedate.getMonth() == 0) {
            year = year - 1;
            month = 12;
        }
        $scope.doing = true;
        $http.get('/expenses/'+ parseInt(year) +'/'+ parseInt(month))
            .success(function(response){
                res = response;
                for(i=0; i<res.length; i++){
                    //$scope.explist[res[i].id] = res[i];
                    splitTags=res[i].tag.split(',');
                    res[i].tags=splitTags;
                    angular.forEach(splitTags, function(value){
                        if ($scope.taglist.indexOf(value) == -1){
                            $scope.taglist.push(value)
                        }
                    });
                }
                //console.log($scope.taglist);
                $scope.doing = false;
                $scope.alerts.push({'type':'success', 'msg':'Got It!!'})
                console.log("Got the data");
            })
            .error(function(what){
                console.log('Fuck!!');
                console.log(what);
                $scope.doing = false;
            });
        
    }
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
                    if (cb)
                        cb(true);
                    $scope.doing = false;
                })
                .error(function(){
                    console.log("delete data Errored");
                    console.log(data);
                    if (cb)
                        cb(false);
                    $scope.doing = false;
                })
            }
        else{
            console.log("unable to delete, Id not found");
        }
    };
    $scope.saveExpense = function(data, cb){
        url = "/expense";
        $scope.doing = true;
        if (data.hasOwnProperty('id')){
            url += '/'+data.id;
            conn = $http.patch(url,data)
                        .success(function(response){
                            response.tags = response.tag.split(',');
                            $scope.explist[$scope.explist.indexOf(data)] = response;
                            //console.log(response);
                            console.log("okay");
                            if (cb)
                                cb(true);
                        $scope.doing = false;
                        });
        }
        else{
            conn = $http.post(url,data)
                        .success(function(response){
                            response.tags = response.tag.split(',');
                            var objdate = response.dateAdded.split('-');

                            if ( (parseInt(objdate[0])) ==( $scope.pagedate.getFullYear() )
                                && parseInt(objdate[1]) == $scope.pagedate.getMonth() + 1) {
                                response.objdateAdded = new Date(res[i].dateAdded);
                                $scope.explist.push(response);
                            }
                            //console.log(response);
                            console.log("okay");
                            $scope.alerts.push({'type':'success', 'msg':'Got It!!'})
                            if (cb)
                                cb(true);
                        $scope.doing = false;
                        });
        }
        conn.error(function(error){
                    console.log("data");
                    console.log(data);
                    console.log("Error");
                    console.log(error);
                    if (cb)
                        cb(false);
                    $scope.doing = false;
                })
    };

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.reload();

})
.directive("expense",function(){
    return{
        retrict:'A',
        scope : {
            ob:"=",
            taglist:"=",
            updateParent:"&",
            deleteParent:"&",
            getMoreTags:"&"
        },
        controller:function($scope){
            $scope.deleting = false;
            $scope.toggleEdit = function(){
                $('#ob'+$scope.ob.id ).collapse('hide');
            };
            $scope.repost = function(edit){
                var dat = $scope.ob;
                var cb = undefined;
                if(!edit){
                    // making a copy, removing from teh original one will make it unidentifiable in future
                    // for edit as well and delete
                    dat = angular.copy(dat);
                    delete(dat.id);
                }
                else{
                    cb = function(done){
                        if(done){
                            $scope.toggleEdit()
                        }
                    }
                }
                if ($scope.ob.tag != $scope.ob.tags.join(",")){
                    dat.tag = $scope.ob.tags.join(",");
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
            },
            $scope.toggletag = function(tvalue, newtag){
                var ind = $scope.ob.tags.indexOf(tvalue);
                if ( ind == -1){
                    $scope.ob.tags.push(tvalue);
                    if(newtag && tvalue!=""){
                        $scope.taglist.push(tvalue);
                        $scope.newtagvalue='';
                    }
                }
                else{
                    $scope.ob.tags.splice(ind, 1);
                }
            }
        },
        templateUrl: ANGULAR_TEMPLATE_PATH +"expense/tmpl/exp_tmpl.html",
    };
})
