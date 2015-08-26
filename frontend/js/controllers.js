'use strict';

/* Controllers */

var metadataEditorApp = angular.module('metadataEditor', ['ui.date']);

// track whether an existing record

// for minification, explicitly declare dependencies $scope and $http
metadataEditorApp.controller('MetadataCtrl', ['$scope', '$http', '$log', 
  function($scope, $http, $log) {

    // initialize list of existing metadata records
    displayAllRecords();

    /**
     * Search for metadata records
     */
    $scope.searchStr = "";
    $scope.search = function()
    { 
        $http.get('http://localhost:4000/api/metadata/search?title=' + 
                  encodeURIComponent($scope.searchStr))
             .success(function(data) {
               $scope.recordsList = data.results; 
             });
    };

    function displayAllRecords()
    {
      $http.get('http://localhost:4000/api/metadata')
           .success(function(data){ 
             $scope.recordsList = data.results; 
           });
    }
  } // end of callback for controller initialization
]);
