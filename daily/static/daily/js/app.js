angular.module('dailyapp', [ 'ui.bootstrap'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller("dailyController",function($scope, $http, $q){
    $scope.uploadorder = function(){
        var cons = []
        for(i=0; i<$scope.dailies.length; i++){
            var daily = $scope.dailies[i];
            if (daily.dirty_order === true ) {
                cons[i] = $http.patch($scope.taskurl + '/' + daily.id,
                    {'order':daily.order}).success(function(daily){return function(respose){
                        daily.dirty_order=false;
                        $scope.alerts.push({
                            'type':'success', 
                            'msg':'Order Update done:' + daily.type})
                            }}(daily)).error(function(respose){
                                $scope.alerts.push({'type':'error', 'msg':'Order Update Failed:'})
                            });
                }
            $q.all(cons).then(function(){
                $scope.dirty_order = false;
            });
        }
    }
    $scope.reload = function(){
        $scope.doing = true
        $scope.alerts = [];
        $scope.dummytype = "dummy";
        $scope.dailyurl = "/daily";
        $scope.taskurl = "/type";

        $http.get($scope.taskurl)
            .success(function(response){
                res = response;
                //console.log(res)
                $scope.dailies = []
                for(i=0; i<res.length; i++){
                    $scope.dailies[res[i].order] = res[i];
                }
                //console.log($scope.taglist);
                $scope.doing = false;
                $scope.alerts.push({'type':'success', 'msg':'Got It!!'})
                //console.log("Got the data");
            })
            .error(function(what){
                console.log('Fuck!!');
                console.log(what);
                $scope.doing = false;
            });
    };

    $scope.newtaskadded = function(daily){
        $scope.dailies[daily.order] = daily;
    }

    $scope.swapdailies = function(daily){
        withdaily = $scope.dailies[daily.order-1]
        $scope.dailies[withdaily.order] = daily;
        $scope.dailies[daily.order] = withdaily;
        withdaily.order += 1
        daily.order -= 1
        withdaily.dirty_order = true
        daily.dirty_order = true
        $scope.dirty_order = true
    }

    $scope.newtaskallowed = function(type){
        for(i=0; i<$scope.dailies.length; i++){
            if ($scope.dailies[i] == type)
                return false
        }
        return true
    }

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.reload();

})
.directive("task",function(){
    return{
        retrict:'A',
        scope : {
            baseurl:"=",
            daily:"=",
            swaporder:"=",
        },
        controller:function($scope, $http){
            $scope.saving = false;
            $scope.newtask = {}; //because ng-if and ng-model dont work well togther,
            $scope.donedates = []; 
            $scope.maxdates = [];
            $scope.todaydate = new Date()
            $scope.caldate = new Date(2017,11,5)

            $scope.getDayClass = function(date,mode){
                console.log(date)
                if ($scope.doneOn({dtstr:date.toDateString()})){
                    return 'full';
                }
                return '';
            }

            for (i=7;i>0;i--){
                dt = new Date();
                dt.setDate($scope.todaydate.getDate()- i);
                $scope.maxdates.push({
                    dtstr : dt.toDateString(),
                    date: dt.getDate()
                });
            }
            $scope.ob = {};
            $scope.ob.id = null;
            $scope.ob.daily = $scope.daily;
            $scope.ob.donetoday = false;


            $scope.doneOn = function(dt){
                for (i=0;i<$scope.donedates.length;i++){
                    //console.log($scope.donedates[i].dtstr , dt.dtstr)
                    if ($scope.donedates[i].dtstr === dt.dtstr){
                        return true;
                    }
                }
                return false;
            }

            $scope.get = function(){
                $scope.saving = true;
                url = $scope.baseurl + "?search=" + $scope.ob.daily.type;
                conn = $http.get(url)
                        .success(function(res){
                            $scope.saving = false;
                            for (i=0; i<res.length;i++){
                                ondate = new Date(res[i].on)
                                if ($scope.todaydate.toDateString() ===  ondate.toDateString()){
                                    $scope.ob.donetoday = true;
                                    $scope.ob.id = res[i].id;
                                }
                                $scope.donedates.push({
                                    dtstr : ondate.toDateString(),
                                    date: ondate.getDate()
                                })
                                //console.log("inside")
                            }
                            //console.log($scope.ob.daily.type,$scope.donedates, res)
                        });
            }

            $scope.toggle = function(){
                $scope.saving = true;
                if ($scope.ob.id === null) {
                    data = {"type_order": $scope.daily.id}
                    //console.log(data)
                    conn = $http.post($scope.baseurl,data)
                            .success(function(response){
                $scope.saving = false;
                                $scope.ob = response;
                                $scope.ob.daily = $scope.daily;
                                $scope.ob.donetoday = $scope.todaydate.toDateString() ==  new Date(response.on).toDateString();
                                //console.log(response);
                                //console.log("okay");
                        });
                }
                else{
                    delurl = $scope.baseurl + '/'+ $scope.ob.id;
                    conn = $http.delete(delurl)
                        .success(function(){
                            $scope.saving = false;
                            $scope.ob = {};
                            $scope.ob.daily = $scope.daily;
                            $scope.ob.id = null;
                            $scope.ob.donetoday = false;
                            //console.log("okay");
                        });
                }
            }
            $scope.get();
        },
        templateUrl: ANGULAR_TEMPLATE_PATH +"daily/tmpl/task_tmpl.html",
    };
})
.directive("dummy",function(){
    return{
        retrict:'A',
        scope : {
            neworder:"&",
            baseurl:"=",
            newtypeadded:"&",
            newtypeallowed:"&"
        },
        controller:function($scope, $http){
            $scope.saving = false;
            $scope.newtask = {}; //because ng-if and ng-model dont work well togther,

            $scope.createtask = function(){
                        posttype = $scope.newtask.type;
                        allowed = $scope.newtypeallowed({type:posttype})
                        if ( allowed !== true){
                            return 0;
                        }
                        data = { "type": posttype, "order":$scope.$parent.dailies.length}
                        $scope.saving = true;
                        conn = $http.post($scope.baseurl,data)
                                .success(function(response){
                                    $scope.saving = false;
                                        $scope.newtypeadded({daily:response});
                                        $scope.newtask.type = '';
                                    //console.log(response);
                                    //console.log("okay");
                            });
                        $scope.saving = false;
            }
        },
        templateUrl: ANGULAR_TEMPLATE_PATH +"daily/tmpl/dummy_tmpl.html",
    };
})
