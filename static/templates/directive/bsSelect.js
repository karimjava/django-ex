app.directive('canvascloud', ['$timeout',function ($timeout) {
        return {
            restrict: 'E',
            scope: {
                items: '='
            },
            templateUrl: '/static/templates/ask/canvas.html',
            link: function (scope, element, attrs) {
                $timeout(function()
                {
                 try {
                      TagCanvas.Start('myCanvas','',{
                        textFont:"DroidSansArabic",
                        shape: "sphere",
                        textColour : '#ff0000',
                        outlineColour : '#ff9999'
                      });
                      TagCanvas.SetSpeed('myCanvas', [0.1, -0.2]);

                  } catch(e) {
                    var x =e;
                  // something went wrong, hide the canvas container
                  }
            }
            ,1000);
        }
    }
}]);

app.directive('bsSelect', function () {

        return {
            restrict: 'E',
            require:'^ngModel',
            scope: {
                items: '=',
                textField: '@',
                valueField: '@',
                ngModel:'='
            },
           templateUrl: '/static/templates/ask/askerTemplate.html',
            link: function (scope, element, attrs, ngModelCtrl) {
              //added a watch to update the text of the multiselect
              scope.$watch('ngModel',function(v){
                scope.setLabel();
              },true);
              //
                var valueField = scope.valueField.toString().trim();
                var textField = scope.textField.toString().trim();
                var modelIsValid = false;
                var selectedItemIsValid = false;

                scope.checkModelValidity = function (items) {
                    if (typeof(items) == "undefined" || !items) return false;
                   if (items.length < 1) return false;
                    return true;
                };
                modelIsValid = scope.checkModelValidity(scope.ngModel);
                scope.setFormValidity = function () {
                    if (typeof (attrs.required) != "undefined") {
                        return modelIsValid;//modelIsValid must be set before we setFormValidity
                    }
                    return true;
                };
                ngModelCtrl.$setValidity('noItemsSet!', scope.setFormValidity());
                scope.checkSelectedItemValidity = function (item) {
                    if (!item) return false;
                    if (!item[valueField]) return false;
                    if (!item[valueField].toString().trim()) return false;
                    return true;
                };

                scope.getItemName = function (item) {
                    return item[textField];
                };


                scope.setLabel = function() {
                    if (typeof (scope.ngModel) =="undefined" || !scope.ngModel || scope.ngModel.length < 1) {

                            scope.currentItemLabel = attrs.defaultText;

                    } else {
                        var allItemsString = '';
                        var selectedItemsCount=scope.ngModel.length;
                         angular.forEach(scope.ngModel, function (item) {
                                    if(item[valueField]=="all")
                                        selectedItemsCount--;
                                });

                        if(selectedItemsCount<2){
                        angular.forEach(scope.ngModel, function (item) {

                                allItemsString = item[textField].toString();

                        });
                        }else{
                            if(selectedItemsCount==2){
                                allItemsString= " لقد قمت باختيار حسابين ";
                            }
                            else
                            {

                                allItemsString= " لقد قمت باختيار " +selectedItemsCount+" حسابات ";
                            }
                        }
                        scope.currentItemLabel = allItemsString;
                    }
                };
                scope.setLabel();
                scope.setCheckboxChecked = function (_item) {
                    var found = false;
                    angular.forEach(scope.ngModel, function (item) {
                        if(item[valueField]=="all")
                        {
                            found=false;

                        }
                        else
                        {
                            if (!found) {
                                if (_item[valueField] === item[valueField]) {
                                   found=true;
                                }
                            }
                        }
                    });
                    return found;
                };
                scope.selectVal = function (_item) {
                    var found = false;
                    if (typeof(scope.ngModel) != "undefined" && scope.ngModel) {
                        for (var i = 0; i < scope.ngModel.length; i++) {
                            if (!found) {
                                if (_item[valueField] === scope.ngModel[i][valueField]) {
                                    found = true;
                                    var index = scope.ngModel.indexOf(scope.ngModel[i]);
                                    scope.ngModel.splice(index, 1);
                                }
                            }
                        }
                    } else {
                        scope.ngModel = [];
                    }
                    if (!found) {
                        scope.ngModel.push(_item);
                    }
                    modelIsValid = scope.checkModelValidity(scope.ngModel);
                    selectedItemIsValid = scope.checkSelectedItemValidity(_item);
                    ngModelCtrl.$setValidity('noItemsSet!', scope.setFormValidity() && selectedItemIsValid);
                    scope.setLabel();
                    ngModelCtrl.$setViewValue(scope.ngModel);
                };

                scope.cancelClose = function($event) {
                    $event.stopPropagation();
                };
            }
        };
    });





