angular.module('managerapp', [ 'ui.bootstrap'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])
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
    $scope.pagedate = new Date(YEAR, MONTH , DAY);
    $scope.doing = 0;

    $scope.load = function(key, year, month){
        $scope.monthlyexps = $scope.monthlyexps || {'data':{}, 'promise':{}};
        console.log(key)
        if ($scope.monthlyexps.promise[key] === undefined){
            $scope.monthlyexps.promise[key] = {}
            $scope.doing+=2;
            $scope.monthlyexps.promise[key].exps = $http.get('/expenses/'+ year +'/'+ month).success(function(){
                $scope.alerts.push({'type':'success', 'msg':'Got Expenses!!'})
                $scope.doing--;
            })
            $scope.monthlyexps.promise[key].tagsums = $http.get('/expense/tagsums?year='+ year +
                '&month='+month).success(function(){
                    $scope.alerts.push({'type':'success', 'msg':'Got TagTotals!!'})
                    $scope.doing--;
                })
        }
        return $scope.monthlyexps.promise[key];
    }

    $scope.reload = function(thedate){
        $scope.explist = [];
        $scope.taglist = [];
        $scope.alerts = [];
        thedate = angular.copy(thedate)
        var year = thedate.getFullYear();  
        var month = parseInt(thedate.getMonth()+1)
        var key = year+'-'+month;
        var prms = $scope.load(key, year, month);
        prms.exps.success(function(response){
                var res = response;
                var explist = [];
                var taglist = [];
                for(i=0; i<res.length; i++){
                    //$scope.explist[res[i].id] = res[i];
                    res[i].objdateAdded = new Date(res[i].dateAdded)
                    explist.push(res[i]);
                    angular.forEach(res[i].tags, function(value){
                        if (taglist.indexOf(value) == -1){
                            taglist.push(value)
                        }
                    });
                }

                $scope.explist = explist;
                $scope.taglist = taglist;
                console.log("Got the data: " + $scope.doing);
            })
            .error(function(what){
                console.log('Fuck!!');
                console.log(what);
                $scope.doing--;
            });

        prms.tagsums.success(function(response){
                $scope.tagsums = response;
                console.log("Got the data: " + $scope.doing);
            })
            .error(function(what){
                console.log('Fuck!!');
                $scope.doing--;
                console.log(what);
            });
        // this call also preloads data for last month, so an extra call to scope.load
        // is not required
        $scope.additionalTags(thedate);
    };
    $scope.additionalTags = function(thedate){
        var year = thedate.getFullYear(),
            month = thedate.getMonth();
        if (thedate.getMonth() == 0) {
            year = year - 1;
            month = 12;
        }
        var key = year+'-'+month;
        prms = $scope.load(key, year, month);
        prms.exps.success(function(response){
                res = response;
                for(i=0; i<res.length; i++){
                    //$scope.explist[res[i].id] = res[i];
                    angular.forEach(res[i].tags, function(value){
                        if ($scope.taglist.indexOf(value) == -1){
                            $scope.taglist.push(value)
                        }
                    });
                }
                //console.log($scope.taglist);
                console.log("Got the data: " + $scope.doing);
            })
            .error(function(what){
                console.log('Fuck!!');
                console.log(what);
                $scope.doing--;
            });
        
    }
    $scope.delExpense = function(data, cb){
        $scope.doing++;
        console.log(data);
        if(data.hasOwnProperty('id')){
            url = '/expense/'+data.id;
            $http.delete(url)
                .success(function(){
                    console.log("okay");
                    //console.log($scope.explist);
                    //console.log(data);
                    $scope.explist.splice($scope.explist.indexOf(data),1);
                    var objdate = data.dateAdded.split('-');
                    var key = parseInt(objdate[0]) + '-' + parseInt(objdate[1]);
                    delete $scope.monthlyexps.promise[key];
                    if (cb)
                        cb(true);
                    $scope.doing--;
                })
                .error(function(){
                    console.log("delete data Errored");
                    console.log(data);
                    if (cb)
                        cb(false);
                    $scope.doing--;
                })
            }
        else{
            console.log("unable to delete, Id not found");
        }
    };
    $scope.saveExpense = function(data, cb){
        url = "/expense";
        $scope.doing++;
        if (data.hasOwnProperty('id')){
            url += '/'+data.id;
            conn = $http.patch(url,data)
                        .success(function(response){
                            var objdate = response.dateAdded.split('-');
                            var key = parseInt(objdate[0]) + '-' + parseInt(objdate[1]);
                            delete $scope.monthlyexps.promise[key];
                            $scope.explist[$scope.explist.indexOf(data)] = response;
                            //console.log(response);
                            console.log("okay");
                            if (cb)
                                cb(true);
                        $scope.doing--;
                        });
        }
        else{
            conn = $http.post(url,data)
                        .success(function(response){
                            var objdate = response.dateAdded.split('-');
                            var key = parseInt(objdate[0]) + '-' + parseInt(objdate[1]);
                            delete $scope.monthlyexps.promise[key];

                            if ( (parseInt(objdate[0])) ==( $scope.pagedate.getFullYear() )
                                && parseInt(objdate[1]) == $scope.pagedate.getMonth() + 1) {
                                response.objdateAdded = new Date(response.dateAdded);
                                $scope.explist.push(response);
                            }
                            //console.log(response);
                            console.log("okay");
                            $scope.alerts.push({'type':'success', 'msg':'Got It!!'})
                            if (cb)
                                cb(true);
                        $scope.doing--;
                        });
        }
        conn.error(function(error){
                    console.log("data");
                    console.log(data);
                    console.log("Error");
                    console.log(error);
                    if (cb)
                        cb(false);
                    $scope.doing--;
                })
    };

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.reload($scope.pagedate);
})
.directive("expense",function(){
    return{
        retrict:'A',
        scope : {
            ob:"=",
            taglist:"=",
            tagsums:"=",
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
