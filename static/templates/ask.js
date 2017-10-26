
var app = angular.module('askApp', ['ezfb','ngSanitize','ui.bootstrap','ui.router']);
  app.run(function($rootScope) {

     $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
          $rootScope.title = toState.title || "لو عندك سؤال";
     });

  });
app.factory("askerList" ,[ '$http', '$q', '$timeout', function ( $http, $q, $timeout) {

    var serv = {};
    serv.askers = null;
    serv.get_askers = function()
    {
        var def = $q.defer();
        if(!serv.askers)
        {
          $http.get("/questions/api/v1/users/").
          success(function(data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                serv.askers =data.results;
                serv.askers.unshift({name:"الكل",image_path:"/static/templates/images/all.png",notShow:true,ask_id:"all",id:"all"});
                // serv.askers.push.apply($scope.askers,data.results);
                def.resolve(serv.askers);


            })
          .error(function(data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                serv.askers = null;
                def.reject()
            });

      }else{
        $timeout(function() {
            def.resolve(serv.askers);
        }, 0)
    }
    return def.promise
  };
  return serv;

}]);

app.controller('azherCtrl',['$scope','$http',function($scope,$http)
{

  $scope.submit =function(result)
  {
    $http.post("/questions/api/v1/results/",result).success(function() {
      $scope.info = "من فضلك تأكد من رقم الجلوس ";
    });
  }

}]);

app.controller('questionCtrl', ['askersData','$scope','$http','$stateParams','$state','$filter',
  function (askersData,$scope,$http,$stateParams,$state,$filter) {



    $scope.category =[
    {
      dangers:["العادة السرية" , "العاده السريه","العاده السرية","العاده السريه","العاده","العادة"],
      color:"rgba(210, 49, 49, 0.89);"
    },
    {love:["مناطق حساسه","المناطق الحساسه","المنطقه الحساسه","المنطقة الحساسة","حب","خطيب","خطيبة","مخطوبه","خطوبه","الرؤية الشرعية","الرؤيه الشرعيه", "الخطوبة","الخطوبه", "عقد","كتب كتاب","مخطوبة","فرح","عقد قران","جواز","زواج" ,"الزواج","حقه الشرعى"],
    color:"rgba(224, 43, 43, 0.52)"},
    {die:["موت","وفاه","توفى","قتل","ذبح","قتال","غيبه","نميمه","ميت"],
    color:"rgba(0, 0, 0, 0.89)"},
    {money:["مال","بنوك","بنك","ميراث","راتب"],
    color:"rgba(207, 210, 5, 0.89)"},
    {pray:["صلاة","قيام الليل","استخاره","ظهر","عصر","مغرب","عشاء","فجر"],
    color:"rgba(32, 146, 36, 0.89)"},
    {maka:["عمره","عمرة","حج","احرام"],
    color:"rgb(56, 185, 142);"},
    {blod:["حيض","نفساء","نفاس","البظر","الاشفار","جنب","جنابة","الحائض","حائض","البريود","بريود","دوره الشهرية","دوره شهريه"],
    color:"rgb(162, 68, 13)"},
    {problem:["تبرج","بنطلون","لحيه","نقاب","هرش","حكه"],
    color:"rgb(169, 115, 142)"},
    {read:["روايه","كتب","كتاب","مرجع","مراجع","دراسه","كليه","كلية","رواية"],
    color:"rgb(88, 136, 195);"}
    ]



    function catogrizeQuestions()
    {
      var found = false
      $scope.questions.forEach(function(question)
      {
        $scope.category.forEach(function (category) {

          if(!found)
          {
            Object.keys(category).forEach(function (key) {
              if(key != 'color')
              {
                category[key].forEach(function(word)
                {
                  if(question.q_html.indexOf(word) > -1 )
                  {
                    question.category = "background-color:"+ category.color;
                  }
                });
              }
            });
          }
        })


      });
    }
    function compressObject(obj) {
      return LZString.compressToEncodedURIComponent(JSON.stringify(obj))
    };

    function decompressObject(str) {
      return JSON.parse(LZString.decompressFromEncodedURIComponent(str))
    };

    $scope.moveToUser = function(user)
    {
      $state.go('questions',{ask_name: user.ask_id})
    }

    function addDataToUrl()
    {

      var ids = [];
      if($scope.asker){
        var allUserIndex=-1;
        $scope.asker.forEach(function(ask,index)
        {
            if(ask)
            {
             if(ask.id =="all")
               allUserIndex = index;

              ids.push(ask.id);
            }
            else
            {
              ids.push("all");
            }

        });

        if(ids.length > 1)
        {
          if(allUserIndex > -1)
            ids.splice(allUserIndex,1);
        }
        if(ids.length >0)
        {
          angular.extend($stateParams, { q: $scope.q, ui:ids, noCancel: true });
          $state.transitionTo('home', $stateParams, { notify: false });
        }
      }

    }

     $scope.getQuestionById = function(id)
    {

      $scope.showLoading = true;
      $http.get("/questions/api/v1/questions/"+id+"/").
      success(function(data, status, headers, config) {
        // this callback will be called asynchronously
        // when the response is available

        $scope.noResult = false;
        $scope.questions = [data];

        if($scope.questions.length == 0)
          $scope.noResult = true;

        catogrizeQuestions();


        $scope.next = data.next;
        $scope.resultCount = data.count;

        addDataToUrl();

        $scope.showLoading = false;
      }).
      error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        $scope.questions = null;
        $scope.showLoading = false;
      });

    };

    $scope.getAskers = function()
    {

       $scope.askers = askersData;

      if(!$stateParams.ui && !$stateParams.ask_name && !$stateParams.id){
        $scope.asker = [askersData[0]];
        $scope.getQuestions();
      }
    };

    $scope.getQuestions = function(q,user_id)
    {
      $scope.showLoading = true;

      var ids = [];

      if(user_id)
      {
        user_id.forEach(function(user)
        {
            if(user)
            {
             if(user.id !="all")
              ids.push(user.id);
            }
            else
            {
              angular.extend($stateParams, { q: $scope.q, ui:"all", noCancel: true });
              $state.transitionTo('home', $stateParams, { notify: false });
            }
        });
      }
      $http.get("/questions/api/v1/questions/", {params:{q:q , filter_by:"q_text",user_id:ids}}).
      success(function(data, status, headers, config) {
        // this callback will be called asynchronously
        // when the response is available
        $scope.noResult = false;
        $scope.questions = data.results;

        if($scope.questions.length == 0)
          $scope.noResult = true;

        catogrizeQuestions();


        $scope.next = data.next;
        $scope.resultCount = data.count;

        addDataToUrl();

        $scope.showLoading = false;
      }).
      error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        $scope.questions = null;
        $scope.showLoading = false;
      });

    }
    var loading = false;
    $scope.getNext = function(q)
    {
      $scope.showLoading = true;
      if(!loading){
        loading = true;
        $http.get(q).success(function(data, status, headers, config) {
        // this callback will be called asynchronously
        // when the response is available
        loading = false;
        if(!$scope.questions)
          $scope.questions=[];

        $scope.questions.push.apply($scope.questions, data.results);
        catogrizeQuestions();

        $scope.resultCount = data.count;
        $scope.next = data.next;
        $scope.showLoading = false;
      }).
        error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        loading = false;
        $scope.showLoading = false;
      });
      }

    }



    // $scope.$watch('askers', function (oldVal, newVal) {
    //   if (oldVal != newVal && askerParams) {

    //     if(askerParams)
    //     {
    //      $scope.asker =[];
    //       askerParams.forEach(function(askerP)
    //       {
    //         var asker = $filter("filter")($scope.askers,{id:askerP})[0];
    //         if(asker)
    //          $scope.asker.push(asker);
    //       });

    //       $scope.getQuestions($scope.q,$scope.asker);
    //       askerParams = false;
    //     }
    //   }
    // });

    if ($stateParams.ask_name) {

      var asker = $filter("filter")(askersData,{ask_id:$stateParams.ask_name})[0];

      if(!asker)
      {
        asker = $filter("filter")(askersData,{ask_id:"all"})[0];
      }

      $scope.asker  = [asker];

      $scope.getQuestions("",$scope.asker);

    }

    else if($stateParams.id)
    {
       $scope.getQuestionById($stateParams.id)
    }

    else if($stateParams.ui) {

      $scope.q = $stateParams.q;

      if($stateParams.ui)
      {
        if(!Array.isArray($stateParams.ui))
          $stateParams.ui = [$stateParams.ui];
      }
      askerParams = $stateParams.ui;

      $scope.asker =[];
      askerParams.forEach(function(askerP)
      {
        var asker = $filter("filter")(askersData,{id:askerP})[0];
        if(asker)
             $scope.asker.push(asker);
      });

      $scope.getQuestions($scope.q,$scope.asker);

    }

  }]);
app.config(['$httpProvider','$stateProvider','$locationProvider','ezfbProvider', function ($httpProvider,$stateProvider,$locationProvider,ezfbProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

  ezfbProvider.setInitParams({
    appId: '1024574047608980',
    version: 'v2.6'
  });

  ezfbProvider.setLocale('ar_AR');

  $locationProvider.html5Mode(true);

  $stateProvider.state('azherResult', {
   url: '/azherResult',
   title:'نتيجة الثانوية الازهريه',
   views: {
    "mainview": {
      templateUrl: '/static/templates/ask/result.html',
      controller: 'azherCtrl'
    },
    resolve: {
      askersData: [ function() {
        debugger
      }]
    },
  }


}).state('home', {
   url: '/?q&ui',
   views: {
    "mainview": {
      templateUrl: '/static/templates/ask/lists.html',
      controller: 'questionCtrl'
    }
  },
   params: {
      q: { squash: true, value: null },
      ui: { squash: true, value: null }
  },
  resolve: {

      askersData: ['askerList', '$q', function(askerList, $q) {

          var def = $q.defer();
          askerList.get_askers().then(function(data) {
            def.resolve(data);
          }, function() {

            def.reject();
          })

          return def.promise;
        }]
    }

}).state('questions', {
   url: '/:ask_name',
   views: {
    "mainview": {
      templateUrl: '/static/templates/ask/lists.html',
      controller: 'questionCtrl'
    },


  },
  resolve: {
    askersData: ['askerList', '$q', function(askerList, $q) {

        var def = $q.defer();
        askerList.get_askers().then(function(data) {

          def.resolve(data);
        }, function() {
          def.reject();
        })

        return def.promise;
      }]
    }

}).state('question', {
   url: '/question/:id',

   views: {
    "mainview": {
      templateUrl: '/static/templates/ask/lists.html',
      controller: 'questionCtrl'
    },


  },
  resolve: {
    askersData: ['askerList', '$q', function(askerList, $q) {

        var def = $q.defer();
        askerList.get_askers().then(function(data) {

          def.resolve(data);
        }, function() {
          def.reject();
        })

        return def.promise;
      }]
    }

});

}]);
app.filter('highlighttextfilter', function() {
  return function(txt,q) {

    return (txt)?txt.replace(q, "<span class='highlightText'>"+q+"</span>"):"";
  };
});
app.filter('localizeNumber',  function () {

  function localeFilterFn(input) {

    var newValue = '';
    var tempStr = String(input);
                // //debugger
                var engStart = "0".charCodeAt(), arStart = "٠".charCodeAt();
                var diff = arStart - engStart;
                for (var i = 0, n = tempStr.length; i < n; i++) {
                  var ch = tempStr.charCodeAt(i);
                  if (ch >= engStart && ch <= (engStart + 9)) {
                    newValue = newValue + String.fromCharCode(ch + diff);
                  }
                  else if (tempStr[i] == '/') {
                    var pre = (tempStr.charCodeAt(i - 1) >= engStart) && (tempStr.charCodeAt(i - 1) <= (engStart + 9))
                    if (i != n - 1) {
                      var post = (tempStr.charCodeAt(i + 1) >= engStart) && (tempStr.charCodeAt(i + 1) <= (engStart + 9))
                    }
                    if(pre && post)
                      newValue += ' / ';
                    else
                      newValue += String.fromCharCode(ch);
                  }
                  else{
                    newValue = newValue + String.fromCharCode(ch);
                  }
                }

                return newValue;
              };
              localeFilterFn.$stateful = true;
              return localeFilterFn;
            });
app.directive('lists', [function () {
  return {
    restrict: 'EA',
    templateUrl: '/static/templates/ask/lists.html',
    controller: 'questionCtrl'
  };
}]);
