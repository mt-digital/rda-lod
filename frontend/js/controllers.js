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
               data = prepareData(data);
               $scope.recordsList = data.results; 
             });
    };

    function displayAllRecords()
    {
      $http.get('http://localhost:4000/api/metadata')
           .success(function(data){ 
             data = prepareData(data);
             $scope.recordsList = data.results; 
           });
    }
    function prepareData(data)
    {
      var results = data.results;
      for (var i=0; i < results.length; i++) 
      {
        var r = results[i];
        if (r.metadata_standards[0].name === 'DDI')
        {
          r.originalLink = 
            'http://www.icpsr.umich.edu/icpsrweb/ICPSR/studies/' +
            r.native_identifier;
        }
      }

      data.results = results;

      return data;
    }
  } // end of callback for controller initialization
]);
