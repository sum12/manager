angular.module('dailyapp', [ 'ui.bootstrap'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller("dailyController",function($scope, $http){
    $scope.reload = function(){
        $scope.doing = true
        $scope.alerts = [];
        $scope.dummytype = "dummy";
        $scope.baseurl = "/daily";
        $http.get($scope.baseurl)
            .success(function(response){
                res = response;
                //console.log(res)
                $scope.dailies = []
                $scope.tasks = []
                for(i=0; i<res.length; i++){
                    $scope.dailies.push(res[i]);
                    if ($scope.tasks.indexOf(res[i].type) == -1){
                        $scope.tasks.push(res[i].type)
                    }
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

    $scope.newtaskadded = function(type){
        if ($scope.tasks.indexOf(type) == -1){
            $scope.tasks.push(type);
        }
    }

    $scope.newtaskallowed = function(type){
        return $scope.tasks.indexOf(type) === -1;
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
            type:"=",
            newtypeadded:"&",
            newtypeallowed:"&"
        },
        controller:function($scope, $http){
            $scope.saving = true;
            $scope.newtask = {}; //because ng-if and ng-model dont work well togther,
            $scope.donedates = []; 
            $scope.maxdates = [];
            $scope.todaydate = new Date()
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
            $scope.ob.type = $scope.type;
            $scope.ob.donetoday = false;


            $scope.doneOn = function(dt){
                for (i=0;i<$scope.donedates.length;i++){
                    if ($scope.donedates[i].dtstr === dt.dtstr){
                        return true;
                    }
                }
                return false;
            }

            $scope.get = function(){
                if ( $scope.type === 'dummy' ){
                    $scope.saving = false;
                    return 0;
                }
                $scope.saving = true;
                url = $scope.baseurl + "?search=" + $scope.ob.type;
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
                            //console.log($scope.ob.type,$scope.donedates, res)
                        })
            }

            $scope.toggle = function(){
                if ($scope.ob.id === null) {
                    posttype = $scope.ob.type;
                    if ( $scope.type === "dummy"){
                        posttype = $scope.newtask.type;
                        allowed = $scope.newtypeallowed({type:posttype})
                        if ( allowed !== true){
                            return 0;
                        }
                    }
                    data = { "type": posttype}
                    //console.log(data)
                    $scope.saving = true;
                    conn = $http.post($scope.baseurl,data)
                            .success(function(response){
                                $scope.saving = false;
                                if ($scope.type !== 'dummy') {
                                    $scope.ob.type = posttype;
                                    $scope.ob.id = response.id;
                                    $scope.ob.donetoday = $scope.todaydate.toDateString() ==  new Date(response.on).toDateString();
                                }
                                else{
                                    $scope.newtypeadded({type:posttype});
                                    $scope.newtask.type = '';
                                }
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
                            $scope.ob.id = null;
                            $scope.ob.type = $scope.type;
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
