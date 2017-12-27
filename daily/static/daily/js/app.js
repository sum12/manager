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
                console.log(res)
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
                console.log("Got the data");
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
            $scope.befores = {}; 
            $scope.ob = {};
            $scope.ob.id = null;
            $scope.ob.type = $scope.type;
            $scope.ob.donetoday = false

            $scope.get = function(){
                if ( $scope.type === 'dummy' ){
                    return
                }
                $scope.saving = true;
                url = $scope.baseurl + "?search=" + $scope.ob.type;
                conn = $http.get(url)
                        .success(function(res){
                            $scope.saving = false;
                            for (i=0; i<res.length;i++){
                                if ( res[i].donetoday === true ){
                                    $scope.ob.id = res[i].id;
                                    $scope.befores.push(res[i].daysbefore)
                                    $scope.ob.donetoday = res[i].donetoday;
                                    console.log($scope.ob)
                                }
                            }
                        })
            }

            $scope.toggle = function(){
                if ($scope.ob.donetoday !== true) {
                    posttype = $scope.ob.type;
                    if ( $scope.type === "dummy"){
                        posttype = $scope.newtask.type;
                        allowed = $scope.newtypeallowed({type:posttype})
                        if ( allowed !== true){
                            return 0;
                        }
                    }
                    data = { "type": posttype}
                    console.log(data)
                    $scope.saving = true;
                    conn = $http.post($scope.baseurl,data)
                            .success(function(response){
                                $scope.saving = false;
                                if ($scope.type !== 'dummy') {
                                    $scope.ob.type = posttype
                                    $scope.ob.id = response.id
                                    $scope.ob.donetoday = response.donetoday
                                }
                                else{
                                    $scope.newtypeadded({type:posttype});
                                    $scope.newtask.type = '';
                                }
                                console.log(response);
                            console.log("okay");
                        });
                }
                else{
                    delurl = $scope.baseurl + '/'+ $scope.ob.id
                    conn = $http.delete(delurl)
                        .success(function(){
                            $scope.saving = false;
                            $scope.ob = {};
                            $scope.ob.id = null;
                            $scope.ob.type = $scope.type;
                            $scope.ob.donetoday = false
                            console.log("okay");
                        });

                }
            }
            $scope.get()
        },
        templateUrl: ANGULAR_TEMPLATE_PATH +"daily/tmpl/task_tmpl.html",
    };
})
