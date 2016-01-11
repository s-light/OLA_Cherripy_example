/******************************************************************************

    slTabbedContent directive

    written by stefan krueger (s-light),
        mail@s-light.eu, http://s-light.eu, https://github.com/s-light/

    havely based on
        https://docs.angularjs.org/guide/directive#creating-directives-that-communicate

    changelog / history
        see git commits

    TO DO:
        ~ enjoy your life :-)

******************************************************************************/

/******************************************************************************

    Copyright 2015 Stefan Krueger

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


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

var slTabbedContent = angular.module('slTabbedContent', [
    // 'xx',
]);

// get current script path
// http://stackoverflow.com/a/21103831/574981
// var scripts = document.getElementsByTagName("script");
// var myDTl_scriptPath = scripts[scripts.length-1].src;
var slTabbedContent_scriptElement = document.querySelector(
    "[src*=slTabbedContent]"
);
var slTabbedContent_scriptPath = slTabbedContent_scriptElement.getAttribute('src');
var slTabbedContent_templateURL = slTabbedContent_scriptPath.replace('.js', '.html');
var slTabbedContent_templateURL_Pane = slTabbedContent_templateURL.replace('.html', '_Pane.html');




slTabbedContent.directive('slTabbedContent', [
    // 'slTabbedContentController',
    '$filter',
function(
    // slTabbedContentController,
    $filter
) { return {
    restrict: 'E',
    transclude: true,
    scope: {
        initialPane: '@',
    },
    // template: '<ul class=""></ul>',
    // templateUrl: 'js/xxx.html',
    // templateUrl: slTabbedContent_templateURL,
    templateUrl: function() {
        // only for development!!!!!
        // this disables the caching of the template file..
        return slTabbedContent_templateURL + '?' + new Date();
    },
    controller:[
        '$scope',
        // '$filter',
        function($scope) {
            // console.log("slTabbedContent");
            // console.log("$scope", $scope);

            var panes = $scope.panes = [];

            /******************************************/
            /** functions **/

            $scope.test = function(event) {
                // console.group("test");
                // console.log("event", event);

                // console.groupEnd();
            };

            $scope.switchToPane = function(pane) {
                // console.group("switchToPane");
                // console.log("pane", pane);
                // deactivate all but given
                angular.forEach(panes, function(paneCurrent, paneIndex){
                    if (paneCurrent == pane) {
                        paneCurrent.active = true;
                    } else {
                        paneCurrent.active = false;
                    }
                });
                // console.groupEnd();
            };

            this.addPane = function(pane) {
                // console.group("addPane");
                // console.log("pane", pane);

                // add new pane to list
                panes.push(pane);

                // show first added pane
                if (pane.title == $scope.initialPane) {
                    $scope.switchToPane(pane);
                }

                // console.log("panes", panes);
                // console.groupEnd();
            };



        }
    ]
};}
]);


slTabbedContent.directive('slPane', [
    '$filter',
    // 'slTabbedContent',
function(
    $filter
    // slTabbedContent
) { return {
    restrict: 'E',
    require: '^slTabbedContent',
    transclude: true,
    scope: {
        title: '@',
    },
    // template: '<ul class=""></ul>',
    // templateUrl: 'something/xxxx.html',
    // templateUrl: slTabbedContent_templateURL_Pane,
    templateUrl: function() {
        // only for development!!!!!
        // this disables the caching of the template file..
        // console.log("slTabbedContent_templateURL_Pane:", slTabbedContent_templateURL_Pane);
        return slTabbedContent_templateURL_Pane + '?' + new Date();
    },
    link: function(scope, element, attr, tabedCtrl) {
        // console.log("slPane");
        // console.log("scope", scope);
        // console.log("element", element);
        // console.log("attrs", attrs);
        // console.log("tabedCtrl", tabedCtrl);

        /******************************************/
        /** functions **/

        // add me to my parent :-)
        tabedCtrl.addPane(scope);

        scope.test = function(event) {
            // console.group("test", event);
            // console.log("testinfo");
            // console.groupEnd();
        };

    }
};}
]);
