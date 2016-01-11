/******************************************************************************

The MIT License (MIT)

Copyright (c) 2015 Stefan Krüger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


******************************************************************************/

var mainControllers = angular.module('mainControllers', [
    // 'myServices',
    'myFilters',
    'slTabbedContent',
    'slInputMods',
    // 'myDirectivesArrays',
    // 'myDirectivesInput',
]);


// MAIN Controller
mainControllers.controller('MainController',[
    // '$scope', '$filter', '$http',
    '$scope', '$http',
    function($scope, $http) {

        //////////////////////////////////////////////////
        // global configuration / default values

        //////////////////////////////////////////////////
        // internal data structure

        $scope.viewStyle = {
            list : {
                'blueocean' : {
                    name : 'blueocean',
                    class : 'blueocean',
                    description : 'deep relaxing blue',
                },
                'sunlight' : {
                    name : 'sunlight',
                    class : 'sunlight',
                    description : 'high contrast - readable by sunlight',
                },
                'test': {
                    name: 'test',
                    class: 'test',
                    description: 'not implementd yet',
                },
            },
            current : {}
        };
        // $scope.viewStyle.current = $scope.viewStyle.list[0];

        // $scope.user = User.user_data();
        $scope.data = {
            settings: {
                // viewStyle: 'blueocean',
                viewStyle: 'sunlight',
            },
            channels: [0],
            channel_id: 1,
        };

        //////////////////////////////////////////
        // functions
        $scope.testThing = function() {
            console.log("testThing");
        };

        $scope.channel_set = function() {
            // console.log("setColorToSelected");
            // console.log("$scope.itemsSelected", $scope.itemsSelected);
            // angular.forEach($scope.itemsSelected, function(item_s, key) {
            //     // console.log("item_s", item_s);
            //     item_s.color.red = $scope.itemActive.color.red;
            //     item_s.color.green = $scope.itemActive.color.green;
            //     item_s.color.blue = $scope.itemActive.color.blue;
            // });
            // console.log("channel_set");
            // post a request to /api/channel/ and update internal list.

            var temp_channel_id = 0;
            var temp_channel_value = 0;

            // console.log("$scope.data.channel_id", $scope.data.channel_id);
            temp_channel_id = $scope.data.channel_id-1;
            temp_channel_value = $scope.data.channels[temp_channel_id];

            // console.log("temp_channel_id", temp_channel_id);
            // console.log("temp_channel_value", temp_channel_value);

            // $http.put(
            //     // url
            //     '/api/channel/',
            //     // data
            //     {
            //         channel_id: temp_channel_id,
            //         channel_value: temp_channel_value,
            //     },
            //     // config
            //     {}
            // ).
            $http(
                // config
                {
                    url: '/api/channel/',
                    method:'PUT',
                    data: {
                        channel_id: temp_channel_id,
                        channel_value: temp_channel_value,
                    },
                }
            ).
            then(
                // success
                function(response) {
                    // console.log("success.");
                    // console.group("success: ");
                    // console.log("response", response);
                    // console.log("response.data", response.data);
                    // console.log("response.status", response.status);
                    // console.groupEnd();
                    // response.status;
                    // $scope.data.channels = response.data;
                    resp_json = response.data;

                    // $scope.data.channels[resp_json.channel_id] =
                    //     resp_json.channel_value;
                },
                // error
                function(response) {
                    console.log("error: ", response);
                    // response.status;
                }
            );
        };

        $scope.channels_get = function() {
            // console.log("channels_get");
            // post a request to /api/channel/ and update internal list.
            $http.get('/api/channel/', {}).
            then(
                // success
                function(response) {
                    console.log("success: ", response);
                    // response.status;
                    $scope.data.channels = response.data;
                },
                // error
                function(response) {
                    console.log("error: ", response);
                    // response.status;
                }
            );
        };

        // channels watch
        // watch example/info http://stackoverflow.com/a/15113029/574981
        // watch deep
        $scope.$watch(
            function(){
                return $scope.data.channels;
            },
            function() {
                // console.log("watch fired.");
                $scope.channel_set();
            },
            true
        );

        //////////////////////////////////////////

        // init channels
        $scope.channels_get();

        //////////////////////////////////////////
    }
]);
