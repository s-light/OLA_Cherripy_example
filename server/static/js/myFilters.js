var myFilters = angular.module('myFilters', []);

// quick JSON formating
myFilters.filter('prettyprint', function() {
    // sames as json filter...but with 4 spaces...
    return function(input) {
        return JSON.stringify(input, null, 4);
    };
});

// quick JSON formating - filtering out all angular internals..
myFilters.filter('angular2json', function() {
    // sames as json filter...but with 4 spaces...
    return function(input) {
        return angular.toJson(input, 4);
    };
});

// http://stackoverflow.com/a/25299523/574981
myFilters.filter('keylength', function(){
    return function(input){
        var result;
        if(angular.isObject(input)){
            result = Object.keys(input).length;
        } else {
            // throw Error("Usage of non-objects with keylength filter!!")
        }
        return result;
    };
});


// print array as list (separator defaults to ', ')
myFilters.filter('list', function(){
    return function(input, separator){
        var result;
        if (!separator) {
            separator = ", ";
        }
        if(angular.isArray(input)){
            result = input.join(separator);
        }
        return result;
    };
});
