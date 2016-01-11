var slInputMods = angular.module('slInputMods', []);

slInputMods.directive('input', function () {
    return {
        restrict: 'E',
        require: 'ngModel',
        link: function (scope, elem, attrs, ctrl) {
            // change output of range to number.
            if (attrs.type.toLowerCase() === 'range') {
                ctrl.$parsers.push(function (value) {
                    var valueAsFloat = parseFloat(value);
                    var returnValue;
                    if (isFinite(valueAsFloat)) {
                        returnValue = valueAsFloat;
                    } else {
                        // don't change model
                        returnValue = ctrl.$modelValue;
                    }
                    return returnValue;
                });
            }
        }
    };
});
